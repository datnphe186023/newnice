<template>
  <div>
    <!-- Hero Banner -->
    <div class="relative bg-gradient-to-br from-gray-900 via-primary-900 to-gray-900 text-white overflow-hidden">
      <div class="absolute inset-0 opacity-10">
        <div class="absolute top-0 right-0 w-96 h-96 bg-primary-400 rounded-full blur-3xl transform translate-x-1/2 -translate-y-1/2" />
        <div class="absolute bottom-0 left-0 w-64 h-64 bg-blue-400 rounded-full blur-2xl transform -translate-x-1/2 translate-y-1/2" />
      </div>
      <div class="container relative py-20 text-center">
        <p class="text-primary-400 font-semibold text-sm uppercase tracking-widest mb-4">
          Về chúng tôi
        </p>
        <h1 class="text-4xl md:text-5xl font-bold mb-6 leading-tight">
          Newnice — Hơn 10 Năm<br />Dẫn Đầu Về Phim Cách Nhiệt
        </h1>
        <p class="text-xl text-white/75 max-w-2xl mx-auto leading-relaxed">
          Chúng tôi không chỉ thi công phim — chúng tôi bảo vệ tài sản và tạo ra
          trải nghiệm lái xe hoàn hảo nhất cho mỗi khách hàng.
        </p>
      </div>
    </div>

    <!-- Story section -->
    <section class="py-16 bg-white">
      <div class="container">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <p class="text-primary-600 font-semibold text-sm uppercase tracking-wider mb-3">
              Câu chuyện của chúng tôi
            </p>
            <h2 class="text-3xl font-bold text-gray-900 mb-6 leading-tight">
              Từ đam mê đến chuyên nghiệp
            </h2>
            <div class="space-y-4 text-gray-600 leading-relaxed">
              <p>
                Newnice được thành lập năm 2014 bởi đội ngũ những người đam mê xe và công nghệ phim.
                Xuất phát từ một xưởng nhỏ tại Nam Từ Liêm, Hà Nội, chúng tôi đã không ngừng học hỏi,
                đầu tư công nghệ và xây dựng đội ngũ kỹ thuật viên giỏi.
              </p>
              <p>
                Hơn 10 năm hoạt động, Newnice đã phục vụ hơn <strong class="text-gray-900">15,000 khách hàng</strong>,
                từ xe phổ thông đến siêu xe cao cấp. Chúng tôi là đại lý ủy quyền chính thức của
                các thương hiệu phim hàng đầu thế giới.
              </p>
              <p>
                Sứ mệnh của chúng tôi: mang đến giải pháp phim cách nhiệt tốt nhất với dịch vụ
                tận tâm và bảo hành uy tín — để mỗi khách hàng ra về với nụ cười hài lòng.
              </p>
            </div>
          </div>

          <!-- Stats -->
          <div class="grid grid-cols-2 gap-4">
            <div
              v-for="stat in stats"
              :key="stat.label"
              class="card p-6 text-center group hover:-translate-y-1 transition-transform"
            >
              <div class="text-4xl font-bold text-primary-600 mb-2">{{ stat.value }}</div>
              <div class="text-sm text-gray-500 font-medium">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Values -->
    <section class="py-16 bg-gray-50">
      <div class="container">
        <div class="text-center mb-12">
          <p class="text-primary-600 font-semibold text-sm uppercase tracking-wider mb-3">
            Giá trị cốt lõi
          </p>
          <h2 class="text-3xl font-bold text-gray-900">Điều làm nên Newnice</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div
            v-for="value in coreValues"
            :key="value.title"
            class="card p-6 text-center group hover:-translate-y-1 transition-transform"
          >
            <div
              class="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-4"
              :class="value.bgColor"
            >
              <component :is="value.icon" class="w-7 h-7" :class="value.iconColor" />
            </div>
            <h3 class="font-bold text-gray-900 mb-2">{{ value.title }}</h3>
            <p class="text-sm text-gray-500 leading-relaxed">{{ value.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Team section -->
    <section class="py-16 bg-white">
      <div class="container">
        <div class="text-center mb-12">
          <p class="text-primary-600 font-semibold text-sm uppercase tracking-wider mb-3">
            Đội ngũ
          </p>
          <h2 class="text-3xl font-bold text-gray-900">Những con người tạo nên Newnice</h2>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div
            v-for="member in team"
            :key="member.name"
            class="card overflow-hidden group"
          >
            <div class="aspect-square bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center">
              <UserCircleIcon class="w-24 h-24 text-primary-400" />
            </div>
            <div class="p-4 text-center">
              <h3 class="font-bold text-gray-900">{{ member.name }}</h3>
              <p class="text-sm text-primary-600 font-medium mt-1">{{ member.role }}</p>
              <p class="text-xs text-gray-500 mt-2 leading-relaxed">{{ member.bio }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Timeline -->
    <section class="py-16 bg-gray-50">
      <div class="container max-w-3xl">
        <div class="text-center mb-12">
          <p class="text-primary-600 font-semibold text-sm uppercase tracking-wider mb-3">
            Hành trình
          </p>
          <h2 class="text-3xl font-bold text-gray-900">Những cột mốc quan trọng</h2>
        </div>

        <div class="relative">
          <!-- Timeline line -->
          <div class="absolute left-8 top-0 bottom-0 w-px bg-primary-200" />

          <div class="space-y-8">
            <div
              v-for="milestone in milestones"
              :key="milestone.year"
              class="relative flex gap-6 items-start"
            >
              <!-- Dot -->
              <div class="w-16 h-16 bg-white border-2 border-primary-300 rounded-full flex items-center justify-center flex-shrink-0 z-10 shadow-sm">
                <span class="text-xs font-bold text-primary-600">{{ milestone.year }}</span>
              </div>
              <!-- Content -->
              <div class="card p-5 flex-1">
                <h3 class="font-bold text-gray-900 mb-1">{{ milestone.title }}</h3>
                <p class="text-sm text-gray-500 leading-relaxed">{{ milestone.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-16 bg-primary-600 text-white text-center">
      <div class="container">
        <h2 class="text-3xl font-bold mb-4">Sẵn sàng trải nghiệm dịch vụ của chúng tôi?</h2>
        <p class="text-white/80 text-lg mb-8 max-w-xl mx-auto">
          Liên hệ ngay để được tư vấn miễn phí và nhận báo giá tốt nhất
        </p>
        <div class="flex flex-wrap gap-4 justify-center">
          <NuxtLink to="/bao-gia" class="bg-white text-primary-600 hover:bg-gray-50 font-semibold px-8 py-3 rounded-xl transition-colors">
            Yêu cầu báo giá
          </NuxtLink>
          <a href="tel:0869418104" class="border-2 border-white/60 hover:border-white text-white font-semibold px-8 py-3 rounded-xl transition-colors">
            📞 0869 418 104
          </a>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import {
  ShieldCheckIcon,
  SparklesIcon,
  UserGroupIcon,
  StarIcon,
  UserCircleIcon,
} from '@heroicons/vue/24/outline'
import { buildOrganizationSchema, useJsonLd } from '~/composables/useJsonLd'
import { useCanonical } from '~/composables/useCanonical'

useSeoMeta({
  title: 'Về chúng tôi | Newnice — Phim cách nhiệt ô tô cao cấp',
  description: 'Newnice — Hơn 10 năm kinh nghiệm trong lĩnh vực phim cách nhiệt ô tô, phim PPF, phim đổi màu xe tại Hà Nội. Đại lý ủy quyền 3M, chuyên nghiệp và uy tín.',
  ogTitle: 'Về Newnice — Hơn 10 năm dẫn đầu phim cách nhiệt',
  ogDescription: 'Hơn 15,000 khách hàng tin tưởng. Đại lý chính hãng 3M, Newnice, PPF. Bảo hành lên đến 10 năm.',
})
useJsonLd(buildOrganizationSchema())
useCanonical('/gioi-thieu')

const stats = [
  { value: '10+', label: 'Năm kinh nghiệm' },
  { value: '15,000+', label: 'Khách hàng hài lòng' },
  { value: '50+', label: 'Dòng sản phẩm' },
  { value: '10 năm', label: 'Bảo hành tối đa' },
]

const coreValues = [
  {
    title: 'Chính hãng 100%',
    desc: 'Tất cả sản phẩm đều có chứng nhận xuất xứ rõ ràng từ nhà sản xuất.',
    icon: ShieldCheckIcon,
    bgColor: 'bg-blue-50',
    iconColor: 'text-blue-600',
  },
  {
    title: 'Kỹ thuật đỉnh cao',
    desc: 'Đội ngũ thi công được đào tạo bài bản, có chứng chỉ quốc tế.',
    icon: SparklesIcon,
    bgColor: 'bg-amber-50',
    iconColor: 'text-amber-600',
  },
  {
    title: 'Khách hàng là trung tâm',
    desc: 'Mọi quyết định đều được đưa ra vì lợi ích tốt nhất cho khách hàng.',
    icon: UserGroupIcon,
    bgColor: 'bg-green-50',
    iconColor: 'text-green-600',
  },
  {
    title: 'Uy tín bảo hành',
    desc: 'Bảo hành minh bạch theo tiêu chuẩn quốc tế, không điều khoản ẩn.',
    icon: StarIcon,
    bgColor: 'bg-purple-50',
    iconColor: 'text-purple-600',
  },
]

const team = [
  {
    name: 'Nguyễn Văn Thắng',
    role: 'Giám đốc điều hành',
    bio: '15 năm kinh nghiệm trong ngành, chuyên gia phim cao cấp được chứng nhận quốc tế.',
  },
  {
    name: 'Trần Thị Lan',
    role: 'Trưởng phòng kỹ thuật',
    bio: 'Chuyên gia thi công PPF và phim ceramic với hơn 8 năm kinh nghiệm thực tiễn.',
  },
  {
    name: 'Lê Hoàng Nam',
    role: 'Tư vấn sản phẩm',
    bio: 'Am hiểu sâu về các dòng phim và nhu cầu của từng loại xe, tư vấn tận tâm.',
  },
  {
    name: 'Phạm Minh Tuấn',
    role: 'Kỹ thuật viên cao cấp',
    bio: 'Chuyên thi công xe cao cấp và siêu xe, tốt nghiệp chương trình 3M Pro.',
  },
]

const milestones = [
  {
    year: '2014',
    title: 'Thành lập Newnice',
    desc: 'Bắt đầu với một xưởng nhỏ tại Nam Từ Liêm, Hà Nội với 3 nhân sự và niềm đam mê lớn.',
  },
  {
    year: '2016',
    title: 'Đại lý ủy quyền 3M',
    desc: 'Trở thành đại lý ủy quyền chính thức của 3M Việt Nam — cột mốc quan trọng đầu tiên.',
  },
  {
    year: '2018',
    title: 'Mở rộng dịch vụ PPF',
    desc: 'Ra mắt dịch vụ dán phim PPF (Paint Protection Film) tại Hà Nội, đầu tiên trong khu vực.',
  },
  {
    year: '2020',
    title: '5,000 khách hàng',
    desc: 'Cột mốc 5,000 khách hàng hài lòng — mở rộng mặt bằng và tuyển thêm kỹ thuật viên.',
  },
  {
    year: '2022',
    title: 'Ra mắt showroom mới',
    desc: 'Khai trương showroom hiện đại 500m², trang thiết bị tiên tiến nhất khu vực.',
  },
  {
    year: '2024',
    title: '15,000+ khách hàng',
    desc: 'Hơn 15,000 khách hàng tin tưởng. Ra mắt website và hệ thống đặt lịch trực tuyến.',
  },
]
</script>
