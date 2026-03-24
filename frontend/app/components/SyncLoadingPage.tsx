'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

interface SyncProgress {
  status: string;
  synced_activities: number;
  total_activities: number;
  progress_percent: number;
  error?: string;
}

interface SyncLoadingPageProps {
  userId: string;
  isFirstSync: boolean;
  onSyncComplete?: () => void;
}

export default function SyncLoadingPage({
  userId,
  isFirstSync,
  onSyncComplete,
}: SyncLoadingPageProps) {
  const router = useRouter();
  const [progress, setProgress] = useState<SyncProgress>({
    status: 'initializing',
    synced_activities: 0,
    total_activities: 0,
    progress_percent: 0,
  });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isFirstSync) {
      // No sync needed, redirect immediately
      onSyncComplete?.();
      router.push('/dashboard');
      return;
    }

    // Poll for sync progress
    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch(`/api/auth/sync/progress/${userId}`);
        const data = (await response.json()) as SyncProgress;
        setProgress(data);

        // Check if sync is complete or errored
        if (data.status === 'completed') {
          clearInterval(pollInterval);
          setTimeout(() => {
            onSyncComplete?.();
            router.push('/dashboard');
          }, 1000);
        } else if (data.status === 'error') {
          clearInterval(pollInterval);
          setError(data.error || 'An error occurred during sync');
        }
      } catch (err) {
        console.error('Error polling sync progress:', err);
      }
    }, 1000); // Poll every second

    return () => clearInterval(pollInterval);
  }, [userId, isFirstSync, router, onSyncComplete]);

  if (!isFirstSync) {
    return null;
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Welcome! 👟</h1>
          <p className="text-gray-600">
            Syncing your running activities from Strava...
          </p>
        </div>

        {error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-700 font-semibold">Error during sync</p>
            <p className="text-red-600 text-sm mt-2">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="mt-4 w-full bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition"
            >
              Try Again
            </button>
          </div>
        ) : (
          <>
            {/* Progress Bar */}
            <div className="mb-6">
              <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-blue-500 to-indigo-600 h-full transition-all duration-300"
                  style={{
                    width: `${Math.min(progress.progress_percent, 100)}%`,
                  }}
                />
              </div>
              <p className="text-center text-sm text-gray-600 mt-3 font-medium">
                {progress.progress_percent.toFixed(0)}% Complete
              </p>
            </div>

            {/* Status Info */}
            <div className="space-y-3 mb-6">
              <div className="flex items-center justify-between">
                <span className="text-gray-700">Status:</span>
                <span className="font-semibold text-indigo-600 capitalize">
                  {progress.status === 'fetching_tokens'
                    ? 'Authenticating'
                    : progress.status === 'fetching_activities'
                      ? 'Fetching activities'
                      : progress.status === 'processing'
                        ? 'Processing'
                        : progress.status === 'finalizing'
                          ? 'Finalizing'
                          : progress.status}
                </span>
              </div>

              {progress.total_activities > 0 && (
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Activities:</span>
                  <span className="font-semibold text-gray-900">
                    {progress.synced_activities} / {progress.total_activities}
                  </span>
                </div>
              )}
            </div>

            {/* Loading Animation */}
            <div className="flex justify-center mb-6">
              <div className="relative w-12 h-12">
                <div className="absolute inset-0 rounded-full border-4 border-gray-200" />
                <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-indigo-600 animate-spin" />
              </div>
            </div>

            <p className="text-center text-sm text-gray-500">
              This may take a few moments. Don't close this page.
            </p>
          </>
        )}
      </div>
    </div>
  );
}
