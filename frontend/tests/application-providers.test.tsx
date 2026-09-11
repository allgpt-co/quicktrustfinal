import { render, screen, cleanup } from '@testing-library/react';
import { afterEach, expect, test, vi } from 'vitest';
import { ApplicationProviders } from '@/providers/application-providers';
const route = vi.hoisted(() => ({ pathname: '/' }));
vi.mock('next/navigation', () => ({ usePathname: () => route.pathname }));
vi.mock('@/providers/auth-provider', () => ({ AuthProvider: ({ children }: { children: React.ReactNode }) => <div data-testid="auth-provider">{children}</div> }));
vi.mock('@/providers/query-provider', () => ({ QueryProvider: ({ children }: { children: React.ReactNode }) => <div data-testid="query-provider">{children}</div> }));
afterEach(cleanup);
test('marketing renders without initializing app authentication', () => {
  route.pathname = '/blog/example';
  render(<ApplicationProviders>Public content</ApplicationProviders>);
  expect(screen.getByText('Public content')).toBeVisible();
  expect(screen.queryByTestId('auth-provider')).toBeNull();
});
test('entering and leaving the app mounts and unmounts its providers', () => {
  route.pathname = '/';
  const view = render(<ApplicationProviders>Content</ApplicationProviders>);
  route.pathname = '/login';
  view.rerender(<ApplicationProviders>Content</ApplicationProviders>);
  expect(screen.getByTestId('auth-provider')).toBeVisible();
  expect(screen.getByTestId('query-provider')).toBeVisible();
  route.pathname = '/';
  view.rerender(<ApplicationProviders>Content</ApplicationProviders>);
  expect(screen.queryByTestId('auth-provider')).toBeNull();
});
