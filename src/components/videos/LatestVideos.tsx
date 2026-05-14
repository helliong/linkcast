import { videos } from "@/data/videos";
import { VideoCard } from "./VideoCard";

export function LatestVideos() {
  return (
    <section id="latest" className="mx-auto max-w-7xl px-6 py-24">
      <div className="mb-12 flex flex-col justify-between gap-5 md:flex-row md:items-end">
        <div>
          <p className="mb-3 text-sm font-medium uppercase tracking-[0.3em] text-cyan-300">
            Latest videos
          </p>

          <h2 className="max-w-2xl text-3xl font-bold tracking-tight text-white md:text-5xl">
            Последние видео, добавленные через Telegram
          </h2>
        </div>

        <p className="max-w-md text-sm leading-6 text-white/60">
          Сейчас данные тестовые. Позже эти карточки будут автоматически
          появляться после отправки ссылки в Telegram-бота.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {videos.map((video) => (
          <VideoCard key={video.id} video={video} />
        ))}
      </div>
    </section>
  );
}