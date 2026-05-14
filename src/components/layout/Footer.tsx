export function Footer() {
  return (
    <footer className="border-t border-white/10 bg-[#070A12]">
      <div className="mx-auto flex max-w-7xl flex-col justify-between gap-6 px-6 py-8 text-sm text-white/50 md:flex-row md:items-center">
        <p>© {new Date().getFullYear()} LinkCast. Video platform powered by Telegram bot. Made by <strong> <a href="https://github.com/helliong">helliong</a></strong></p>

        <div className="flex gap-5">
          <a href="https://t.me/linkcast_video_bot" className="transition hover:text-white">
            Telegram
          </a>
          <a href="https://github.com/helliong/linkcast" className="transition hover:text-white">
            GitHub
          </a>
        </div>
      </div>
    </footer>
  );
}