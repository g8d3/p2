import { type ClassValue, clsx } from "clsx";

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

export function formatBps(value: number): string {
  return `${value.toFixed(1)} bps`;
}

export function formatPercentage(value: number): string {
  return `${(value / 100).toFixed(2)}%`;
}

export function formatApy(value: number): string {
  return `${value.toFixed(0)}% APY`;
}

export function formatVolume(value: number): string {
  if (value >= 1000000) {
    return `$${(value / 1000000).toFixed(1)}M`;
  } else if (value >= 1000) {
    return `$${(value / 1000).toFixed(1)}K`;
  }
  return `$${value.toFixed(0)}`;
}

export function formatTimeUntil(date: Date): string {
  const now = new Date();
  const diff = date.getTime() - now.getTime();
  
  if (diff < 0) return 'Past due';
  
  const hours = Math.floor(diff / 3600000);
  const minutes = Math.floor((diff % 3600000) / 60000);
  
  if (hours > 0) {
    return `${hours}h ${minutes}m`;
  }
  return `${minutes}m`;
}

export function normalizeIntervalRate(rate: number, interval: number): number {
  // Normalize to 8-hour rate for comparison
  return (rate * 8) / interval;
}
