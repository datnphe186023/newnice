"""
Email notification service.

Uses stdlib smtplib wrapped in asyncio.get_event_loop().run_in_executor()
so it doesn't block the async event loop. No extra dependencies required.

When SMTP is not configured (EMAIL_HOST is empty), all sends are silently
skipped and a warning is logged — this way the app works in dev without
any email setup.
"""

import asyncio
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import partial
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Low-level SMTP helpers (run in threadpool to avoid blocking)
# ---------------------------------------------------------------------------

def _send_via_smtp(
    to_email: str,
    subject: str,
    html_body: str,
    text_body: str = "",
) -> None:
    """Synchronous SMTP send — called inside run_in_executor."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>"
    msg["To"] = to_email

    if text_body:
        msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    if settings.EMAIL_USE_TLS:
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            server.send_message(msg)
    else:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.ehlo()
            if settings.EMAIL_USE_STARTTLS:
                server.starttls()
            if settings.EMAIL_USERNAME:
                server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            server.send_message(msg)


async def send_email(
    to_email: str,
    subject: str,
    html_body: str,
    text_body: str = "",
) -> bool:
    """
    Send an email asynchronously.
    Returns True on success, False if unconfigured or on error.
    """
    if not settings.EMAIL_HOST:
        logger.debug("EMAIL_HOST not set — skipping email send to %s", to_email)
        return False

    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(
            None,
            partial(_send_via_smtp, to_email, subject, html_body, text_body),
        )
        logger.info("Email sent to %s: %s", to_email, subject)
        return True
    except Exception as exc:
        logger.error("Failed to send email to %s: %s", to_email, exc)
        return False


async def send_to_multiple(
    recipients: list[str],
    subject: str,
    html_body: str,
    text_body: str = "",
) -> None:
    """Send the same email to multiple recipients concurrently."""
    await asyncio.gather(
        *[send_email(r, subject, html_body, text_body) for r in recipients],
        return_exceptions=True,
    )


# ---------------------------------------------------------------------------
# Email templates
# ---------------------------------------------------------------------------

def _base_html(title: str, content: str) -> str:
    """Wrap content in a simple branded HTML shell."""
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{title}</title>
</head>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:Inter,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:40px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0"
             style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08);">
        <!-- Header -->
        <tr>
          <td style="background:linear-gradient(135deg,#2563eb,#1d4ed8);padding:32px 40px;text-align:center;">
            <h1 style="margin:0;color:#ffffff;font-size:24px;font-weight:700;">Newnice</h1>
            <p style="margin:4px 0 0;color:rgba(255,255,255,.8);font-size:13px;">
              Phim cách nhiệt ô tô cao cấp
            </p>
          </td>
        </tr>
        <!-- Body -->
        <tr>
          <td style="padding:40px;">
            {content}
          </td>
        </tr>
        <!-- Footer -->
        <tr>
          <td style="background:#f8fafc;padding:24px 40px;text-align:center;
                     border-top:1px solid #e2e8f0;">
            <p style="margin:0;color:#94a3b8;font-size:12px;">
              © 2024 Newnice · 123 Nguyễn Văn Linh, Quận 7, TP.HCM<br/>
              <a href="tel:0869418104" style="color:#2563eb;">0869 418 104</a> ·
              <a href="mailto:newnicefilm@gmail.com" style="color:#2563eb;">newnicefilm@gmail.com</a>
            </p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


def _row(label: str, value: Optional[str]) -> str:
    if not value:
        return ""
    return f"""
    <tr>
      <td style="padding:8px 0;color:#64748b;font-size:14px;width:40%;">{label}</td>
      <td style="padding:8px 0;color:#1e293b;font-size:14px;font-weight:500;">{value}</td>
    </tr>"""


# ---------------------------------------------------------------------------
# Quote request emails
# ---------------------------------------------------------------------------

async def notify_new_quote(
    customer_name: str,
    phone: str,
    email: Optional[str],
    car_brand: Optional[str],
    car_model: Optional[str],
    car_year: Optional[int],
    service_type: Optional[str],
    film_type_preference: Optional[str],
    message: Optional[str],
) -> None:
    """Send admin notification + optional customer confirmation for a new quote."""
    # --- Admin notification ---
    admin_content = f"""
    <h2 style="margin:0 0 8px;color:#1e293b;font-size:20px;">📋 Yêu cầu báo giá mới</h2>
    <p style="margin:0 0 24px;color:#64748b;font-size:14px;">
      Khách hàng vừa gửi yêu cầu báo giá trên website.
    </p>
    <table width="100%" cellpadding="0" cellspacing="0"
           style="border:1px solid #e2e8f0;border-radius:8px;border-collapse:collapse;overflow:hidden;">
      <tr style="background:#f8fafc;">
        <td colspan="2" style="padding:12px 16px;font-weight:600;color:#1e293b;font-size:14px;">
          Thông tin khách hàng
        </td>
      </tr>
      <tbody style="padding:0 16px;">
        {_row("Họ tên", customer_name)}
        {_row("Điện thoại", f'<a href="tel:{phone}" style="color:#2563eb;">{phone}</a>')}
        {_row("Email", email)}
        {_row("Hãng xe", car_brand)}
        {_row("Dòng xe", car_model)}
        {_row("Năm sản xuất", str(car_year) if car_year else None)}
        {_row("Dịch vụ quan tâm", service_type)}
        {_row("Loại phim", film_type_preference)}
        {_row("Ghi chú", message)}
      </tbody>
    </table>
    <div style="margin-top:24px;text-align:center;">
      <a href="{settings.ADMIN_URL}/admin/quotes"
         style="display:inline-block;background:#2563eb;color:#fff;padding:12px 28px;
                border-radius:8px;text-decoration:none;font-weight:600;font-size:14px;">
        Xem trong Admin →
      </a>
    </div>
    """
    await send_email(
        to_email=settings.ADMIN_EMAIL,
        subject=f"[Newnice] Báo giá mới từ {customer_name} – {phone}",
        html_body=_base_html("Yêu cầu báo giá mới", admin_content),
        text_body=(
            f"Báo giá mới từ {customer_name} ({phone}).\n"
            f"Xe: {car_brand} {car_model} {car_year or ''}\n"
            f"Dịch vụ: {service_type or 'Chưa chọn'}\n"
            f"Tin nhắn: {message or 'Không có'}"
        ),
    )

    # --- Customer confirmation (only if email provided) ---
    if email:
        customer_content = f"""
        <h2 style="margin:0 0 8px;color:#1e293b;font-size:20px;">
          Cảm ơn bạn, {customer_name}! 🎉
        </h2>
        <p style="margin:0 0 16px;color:#475569;font-size:15px;line-height:1.6;">
          Chúng tôi đã nhận được yêu cầu báo giá của bạn và sẽ liên hệ lại
          trong vòng <strong>30 phút</strong> (trong giờ làm việc).
        </p>
        <div style="background:#eff6ff;border-left:4px solid #2563eb;
                    border-radius:0 8px 8px 0;padding:16px;margin-bottom:24px;">
          <p style="margin:0;color:#1d4ed8;font-size:14px;font-weight:500;">
            Thông tin bạn đã gửi:
          </p>
          <ul style="margin:8px 0 0;padding-left:20px;color:#475569;font-size:14px;">
            <li>Điện thoại: <strong>{phone}</strong></li>
            {"<li>Xe: <strong>" + str(car_brand or "") + " " + str(car_model or "") + "</strong></li>" if car_brand else ""}
            {"<li>Dịch vụ: <strong>" + str(service_type) + "</strong></li>" if service_type else ""}
          </ul>
        </div>
        <p style="margin:0 0 16px;color:#475569;font-size:14px;">
          Nếu cần hỗ trợ gấp, hãy gọi thẳng cho chúng tôi:
        </p>
        <div style="text-align:center;">
          <a href="tel:0869418104"
             style="display:inline-block;background:#f59e0b;color:#fff;padding:12px 28px;
                    border-radius:8px;text-decoration:none;font-weight:700;font-size:16px;">
            📞 0901 234 567
          </a>
        </div>
        """
        await send_email(
            to_email=email,
            subject="[Newnice] Đã nhận yêu cầu báo giá của bạn",
            html_body=_base_html("Xác nhận yêu cầu báo giá", customer_content),
            text_body=(
                f"Xin chào {customer_name},\n\n"
                "Chúng tôi đã nhận được yêu cầu báo giá của bạn và sẽ liên hệ "
                "trong vòng 30 phút (giờ hành chính).\n\n"
                "Hotline: 0869 418 104\n"
                "Email: newnicefilm@gmail.com"
            ),
        )


# ---------------------------------------------------------------------------
# Contact message emails
# ---------------------------------------------------------------------------

async def notify_new_contact(
    name: str,
    email: str,
    phone: Optional[str],
    subject: Optional[str],
    message: str,
) -> None:
    """Send admin notification + customer confirmation for a contact message."""
    # --- Admin notification ---
    admin_content = f"""
    <h2 style="margin:0 0 8px;color:#1e293b;font-size:20px;">✉️ Tin nhắn liên hệ mới</h2>
    <p style="margin:0 0 24px;color:#64748b;font-size:14px;">
      Khách hàng vừa gửi tin nhắn qua form liên hệ.
    </p>
    <table width="100%" cellpadding="0" cellspacing="0"
           style="border:1px solid #e2e8f0;border-radius:8px;border-collapse:collapse;">
      <tr style="background:#f8fafc;">
        <td colspan="2" style="padding:12px 16px;font-weight:600;color:#1e293b;font-size:14px;">
          Chi tiết tin nhắn
        </td>
      </tr>
      <tbody style="padding:0 16px;">
        {_row("Họ tên", name)}
        {_row("Email", f'<a href="mailto:{email}" style="color:#2563eb;">{email}</a>')}
        {_row("Điện thoại", f'<a href="tel:{phone}" style="color:#2563eb;">{phone}</a>' if phone else None)}
        {_row("Chủ đề", subject)}
      </tbody>
    </table>
    <div style="margin:16px 0;background:#f8fafc;border:1px solid #e2e8f0;
                border-radius:8px;padding:16px;">
      <p style="margin:0 0 8px;color:#64748b;font-size:13px;font-weight:500;">Nội dung:</p>
      <p style="margin:0;color:#1e293b;font-size:14px;line-height:1.7;white-space:pre-wrap;">{message}</p>
    </div>
    <div style="text-align:center;">
      <a href="mailto:{email}?subject=Re: {subject or 'Liên hệ từ website'}"
         style="display:inline-block;background:#2563eb;color:#fff;padding:12px 28px;
                border-radius:8px;text-decoration:none;font-weight:600;font-size:14px;">
        Trả lời email →
      </a>
    </div>
    """
    await send_email(
        to_email=settings.ADMIN_EMAIL,
        subject=f"[Newnice] Liên hệ mới từ {name} – {subject or 'Không có chủ đề'}",
        html_body=_base_html("Tin nhắn liên hệ mới", admin_content),
        text_body=f"Liên hệ mới từ {name} ({email}).\nChủ đề: {subject or '-'}\n\n{message}",
    )

    # --- Customer confirmation ---
    customer_content = f"""
    <h2 style="margin:0 0 8px;color:#1e293b;font-size:20px;">
      Đã nhận tin nhắn của bạn, {name}!
    </h2>
    <p style="margin:0 0 16px;color:#475569;font-size:15px;line-height:1.6;">
      Cảm ơn bạn đã liên hệ với Newnice. Chúng tôi sẽ phản hồi trong vòng
      <strong>24 giờ làm việc</strong>.
    </p>
    <div style="background:#f0fdf4;border-left:4px solid #22c55e;
                border-radius:0 8px 8px 0;padding:16px;margin-bottom:24px;">
      <p style="margin:0;color:#15803d;font-size:14px;">
        ✅ Tin nhắn của bạn đã được ghi nhận thành công.
      </p>
    </div>
    <p style="margin:0 0 16px;color:#475569;font-size:14px;">
      Trong thời gian chờ đợi, bạn có thể khám phá các sản phẩm của chúng tôi
      hoặc gọi hotline nếu cần hỗ trợ ngay:
    </p>
    <div style="text-align:center;">
      <a href="tel:0869418104"
         style="display:inline-block;background:#2563eb;color:#fff;padding:12px 28px;
                border-radius:8px;text-decoration:none;font-weight:600;font-size:14px;margin-right:8px;">
        📞 Gọi ngay
      </a>
      <a href="{settings.SITE_URL}/san-pham"
         style="display:inline-block;border:2px solid #2563eb;color:#2563eb;padding:10px 28px;
                border-radius:8px;text-decoration:none;font-weight:600;font-size:14px;">
        Xem sản phẩm
      </a>
    </div>
    """
    await send_email(
        to_email=email,
        subject="[Newnice] Đã nhận tin nhắn của bạn",
        html_body=_base_html("Xác nhận liên hệ", customer_content),
        text_body=(
            f"Xin chào {name},\n\n"
            "Chúng tôi đã nhận được tin nhắn của bạn và sẽ phản hồi trong "
            "vòng 24 giờ làm việc.\n\n"
            "Hotline: 0869 418 104\n"
            "Email: newnicefilm@gmail.com"
        ),
    )
