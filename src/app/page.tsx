import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { LatestVideos } from "@/components/videos/LatestVideos";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#070A12]">
      <Header />
      <div className="absolute left-1/2 top-30 h-[500px] w-[500px] -translate-x-1/2 rounded-full bg-cyan-500/20 blur-[120px]" />
      <div className="absolute right-5 top-100 h-[400px] w-[400px] rounded-full bg-violet-500/20 blur-[120px]" />
      <section className="relative overflow-hidden px-6 py-24 md:py-32">
        <div className="relative mx-auto max-w-7xl">
          <div className="max-w-3xl">
            <h1 className="mb-6 text-5xl font-bold tracking-tight text-white md:text-7xl">
              Видео-платформа, где контент добавляется через{" "}
              <span className="bg-gradient-to-r from-cyan-300 to-violet-400 bg-clip-text text-transparent">
                Telegram-бота
              </span>
            </h1>

            <p className="mb-10 max-w-2xl text-lg leading-8 text-white/60">
              Отправляй ссылки на видео через нашего Telegram-бота, и после
              модерации они появятся на сайте для всех пользователей. Легко,
              быстро и удобно!
            </p>

            <div className="flex flex-col gap-4 sm:flex-row">
              <a
                href="#latest"
                className="rounded-full bg-cyan-400 px-7 py-4 text-center text-sm font-semibold text-black transition hover:bg-cyan-300"
              >
                Смотреть видео
              </a>

              <a
                href="https://t.me/linkcast_video_bot"
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-full border border-white/10 bg-white/5 px-7 py-4 text-center text-sm font-semibold text-white transition hover:bg-white/10"
              >
                Отправить видео
              </a>
            </div>
          </div>
        </div>
      </section>

      <LatestVideos />

      <Footer />
    </main>
  );
}
