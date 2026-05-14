export type VideoPlatform = "youtube" | "rutube" | "vk video" | "unknown";

export type VideoStatus = "pending" | "approved" | "rejected" | "deleted";

export interface Video {
  id: string;
  title: string;
  description: string;
  url: string;
  embedUrl: string;
  thumbnailUrl: string;
  platform: VideoPlatform;
  category: string;
  status: VideoStatus;
  duration: number | null;
  uploader: string | null;
  addedByTelegramId: number;
  addedByUsername: string | null;
  createdAt: string;
}