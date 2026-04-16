<template>
  <footer class="bg-dark text-white">
    <!-- Main footer -->
    <div class="container py-12">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <!-- Company info -->
        <div>
          <h3 class="mb-4">
            <img src="/logo.png" alt="Newnice" class="h-14 w-auto" />
          </h3>
          <p class="text-gray-300 mb-4">
            Chuyên cung cấp và thi công phim cách nhiệt ô tô Newnice và PPF bảo vệ sơn xe tại Hà Nội. Chất lượng chính hãng, bảo hành dài hạn.
          </p>
          <div class="flex gap-3">
            <a href="https://facebook.com/newnicevn" target="_blank" rel="noopener" class="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-accent transition-colors">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M18.77,7.46H14.5v-1.9c0-.9.6-1.1,1-1.1h3V.5h-4.33C10.24.5,9.5,3.44,9.5,5.32v2.15h-3v4h3v12h5v-12h3.85l.42-4Z"/></svg>
            </a>
            <a href="#" class="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-accent transition-colors">
              <span class="sr-only">YouTube</span>
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M23.5,6.19a3.02,3.02,0,0,0-2.12-2.14C19.58,3.5,12,3.5,12,3.5s-7.58,0-9.38.55A3.02,3.02,0,0,0,.5,6.19,31.56,31.56,0,0,0,0,12a31.56,31.56,0,0,0,.5,5.81,3.02,3.02,0,0,0,2.12,2.14c1.8.55,9.38.55,9.38.55s7.58,0,9.38-.55a3.02,3.02,0,0,0,2.12-2.14A31.56,31.56,0,0,0,24,12,31.56,31.56,0,0,0,23.5,6.19ZM9.55,15.57V8.43L15.82,12Z"/></svg>
            </a>
            <a href="https://zalo.me/0705410751" target="_blank" rel="noopener" class="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-accent transition-colors">
              <span class="sr-only">Zalo</span>
              <span class="font-bold text-sm">Zalo</span>
            </a>
          </div>
        </div>

        <!-- Products -->
        <div>
          <h4 class="text-lg font-semibold mb-4">Sản phẩm</h4>
          <ul class="space-y-2">
            <li>
              <NuxtLink to="/danh-muc/phim-cach-nhiet-newnice" class="text-gray-300 hover:text-accent transition-colors">
                Phim cách nhiệt Newnice
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/danh-muc/ppf-newnice" class="text-gray-300 hover:text-accent transition-colors">
                PPF Newnice
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/san-pham" class="text-gray-300 hover:text-accent transition-colors">
                Tất cả sản phẩm
              </NuxtLink>
            </li>
          </ul>
        </div>

        <!-- Quick links -->
        <div>
          <h4 class="text-lg font-semibold mb-4">Liên kết</h4>
          <ul class="space-y-2">
            <li>
              <NuxtLink to="/tin-tuc" class="text-gray-300 hover:text-accent transition-colors">
                Tin tức
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/bao-gia" class="text-gray-300 hover:text-accent transition-colors">
                Báo giá
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/lien-he" class="text-gray-300 hover:text-accent transition-colors">
                Liên hệ
              </NuxtLink>
            </li>
          </ul>
        </div>

        <!-- Contact -->
        <div>
          <h4 class="text-lg font-semibold mb-4">Liên hệ</h4>
          <ul class="space-y-3">
            <li class="flex items-start gap-3">
              <MapPinIcon class="w-5 h-5 text-accent flex-shrink-0 mt-0.5" />
              <span class="text-gray-300">311 Phúc Diễn, Nam Từ Liêm, Hà Nội</span>
            </li>
            <li class="flex items-center gap-3">
              <PhoneIcon class="w-5 h-5 text-accent flex-shrink-0" />
              <a href="tel:0869418104" class="text-gray-300 hover:text-accent transition-colors">
                0869 418 104
              </a>
            </li>
            <li class="flex items-center gap-3">
              <EnvelopeIcon class="w-5 h-5 text-accent flex-shrink-0" />
              <a href="mailto:newnicefilm@gmail.com" class="text-gray-300 hover:text-accent transition-colors">
                newnicefilm@gmail.com
              </a>
            </li>
            <li class="flex items-center gap-3">
              <ClockIcon class="w-5 h-5 text-accent flex-shrink-0" />
              <span class="text-gray-300">8:00 - 18:00 (T2 - CN)</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Bottom bar -->
    <div class="border-t border-white/10 py-4">
      <div class="container text-center text-gray-400 text-sm">
        <p>© {{ currentYear }} Newnice. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { MapPinIcon, PhoneIcon, EnvelopeIcon, ClockIcon } from '@heroicons/vue/24/outline'

const currentYear = new Date().getFullYear()
</script>
