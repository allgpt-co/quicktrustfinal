import type { Metadata } from 'next';
import { DIRECTORY_ORIGIN } from './compliance-directory';

export function directoryMetadata(
  title: string,
  description: string,
  path: string,
  index = false,
): Metadata {
  return {
    title,
    description,
    alternates: { canonical: DIRECTORY_ORIGIN + path },
    robots: { index, follow: true },
    openGraph: { title, description, url: DIRECTORY_ORIGIN + path, type: 'website' },
    twitter: { title, description, card: 'summary_large_image' },
  };
}
