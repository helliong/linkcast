"use client";

import { useEffect, useState } from "react";
import { VideoCard } from "./VideoCard";
import type { Video } from "@/types/video";

export function LatestVideos() {
  const [videos, setVideos] = useState<Video[]>([]);

  useEffect(() => {
    async function loadVideos() {
      const response = await fetch("/data/videos.json", {
        cache: "no-store",
      });

      const data: Video[] = await response.json();

      setVideos(data.filter((video) => video.status === "approved"));
    }

    loadVideos();
  }, []);

  return (
    <section id="latest" className="mx-auto max-w-7xl px-6 py-24">
      <div className="mb-12 flex flex-col justify-between gap-5 md:flex-row md:items-end">
        <div>
          <p className="mb-3 text-sm font-medium uppercase tracking-[0.3em] text-cyan-300">
            Latest videos
          </p>

          <h2 className="max-w-2xl text-3xl font-bold tracking-tight text-white md:text-5xl">
            Последние одобренные видео
          </h2>
        </div>

        <p className="max-w-md text-sm leading-6 text-white/60">
          Эти видео были отправлены через Telegram-бота и одобрены модератором.
        </p>
      </div>

      {videos.length > 0 ? (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {videos.map((video) => (
            <VideoCard key={video.id} video={video} />
          ))}
        </div>
      ) : (
        <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-10 text-center">
          <h3 className="mb-3 text-xl font-semibold text-white">
            Пока нет одобренных видео
          </h3>

          <p className="text-sm text-white/60">
            Отправь ссылку через Telegram-бота, после модерации она появится
            здесь.
          </p>
        </div>
      )}
    </section>
  );
}