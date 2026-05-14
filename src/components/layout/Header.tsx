export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-[#070A12]/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
        <a href="/" className="text-xl font-bold tracking-tight text-white">
          Link<span className="text-cyan-400">Cast</span>
        </a>

        <a
          href="https://t.me/linkcast_video_bot"
          target="_blank"
          rel="noopener noreferrer"
          className="rounded-full border border-white/10 bg-white/10 px-5 py-2 text-sm font-medium text-white transition hover:bg-white/15"
        >
          Отправить видео
        </a>
      </div>
    </header>
  );
}
