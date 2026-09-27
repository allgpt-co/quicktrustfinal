'use client';
import { trackDirectoryEvent, type DirectoryEvent } from '@/lib/marketing-analytics';
import type { ReactNode } from 'react';

export default function DirectoryActionLink({
  href,
  children,
  event = 'directory_source_click',
  className = '',
}: {
  href: string;
  children: ReactNode;
  event?: DirectoryEvent;
  className?: string;
}) {
  return (
    <a href={href} className={className} onClick={() => trackDirectoryEvent(event)}>
      {children}
    </a>
  );
}
