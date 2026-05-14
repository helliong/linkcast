import type { Video } from "@/types/video";

interface VideoCardProps {
  video: Video;
}

export function VideoCard({ video }: VideoCardProps) {
  return (
    <article className="group overflow-hidden rounded-3xl border border-white/10 bg-white/[0.04] transition hover:-translate-y-1 hover:bg-white/[0.07]">
      <a href={video.url} target="_blank" rel="noopener noreferrer">
        <div className="relative aspect-video overflow-hidden bg-white/5">
          <img
            src={video.thumbnailUrl}
            alt={video.title}
            className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
          />

          <div className="absolute left-4 top-4 rounded-full bg-black/60 px-3 py-1 text-xs font-medium text-white backdrop-blur">
            {video.platform}
          </div>

          <div className="absolute inset-0 flex items-center justify-center bg-black/20 opacity-0 transition group-hover:opacity-100">
            <div className="flex h-14 w-14 items-center justify-center rounded-full bg-white text-black">
              ▶
            </div>
          </div>
        </div>

        <div className="p-5">
          <div className="mb-3 flex items-center justify-between gap-3">
            <span className="rounded-full bg-cyan-400/10 px-3 py-1 text-xs font-medium text-cyan-300">
              {video.category}
            </span>

            <span className="text-xs text-white/40">{video.createdAt}</span>
          </div>

          <h3 className="mb-2 text-lg font-semibold text-white">
            {video.title}
          </h3>

          <p className="line-clamp-2 text-sm leading-6 text-white/60">
            {video.description}
          </p>
        </div>
      </a>
    </article>
  );
}
