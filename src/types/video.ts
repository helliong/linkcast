export type VideoPlatform = "youtube" | "rutube" | "vk" | "other";

export type VideoStatus = "pending" | "approved" | "rejected" | "deleted" | "broken";

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
  authorName: string;
  createdAt: string;
}