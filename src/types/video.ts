export type VideoPlatform = "youtube" | "rutube" | "vk" | "other";

export interface Video {
  id: string;
  title: string;
  description: string;
  url: string;
  embedUrl: string;
  thumbnailUrl: string;
  platform: VideoPlatform;
  category: string;
  createdAt: string;
}