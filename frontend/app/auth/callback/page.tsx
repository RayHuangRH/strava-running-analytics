'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import {
  Box,
  Center,
  VStack,
  Spinner,
  Heading,
  Text,
  Link as ChakraLink,
} from '@chakra-ui/react';
import SyncLoadingPage from '../../components/SyncLoadingPage';
import { jwtDecode } from 'jwt-decode';

interface TokenPayload {
  athlete_id: number;
  sub?: string;
}

export default function AuthCallback() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [shouldShowSync, setShouldShowSync] = useState(false);
  const [isFirstSync, setIsFirstSync] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const handleCallback = async () => {
      try {
        const code = searchParams.get('code');
        const state = searchParams.get('state');

        if (!code) {
          setError('No authorization code received from Strava');
          setLoading(false);
          return;
        }

        // Exchange auth code for access token via backend
        const response = await fetch(
          'http://localhost:8000/api/auth/strava/callback',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code, state }),
            credentials: 'include',
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to authenticate');
        }

        const data = await response.json();

        // Store tokens in localStorage (or cookies for production)
        localStorage.setItem('accessToken', data.accessToken);
        localStorage.setItem('athleteData', JSON.stringify(data.athlete));

        // Decode JWT to get user_id
        try {
          const decoded = jwtDecode<TokenPayload>(data.accessToken);
          const userIdFromToken = decoded.sub || decoded.athlete_id?.toString();

          if (userIdFromToken) {
            setUserId(userIdFromToken);
          }
        } catch (decodeError) {
          console.error('Failed to decode token:', decodeError);
        }

        // Check if we need to show sync loading page
        if (data.should_sync && data.is_first_sync) {
          setShouldShowSync(true);
          setIsFirstSync(true);
          setLoading(false);
        } else {
          setLoading(false);
          router.push('/dashboard');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error occurred');
        setLoading(false);
      }
    };

    handleCallback();
  }, [searchParams, router]);

  // Show sync loading page if needed
  if (shouldShowSync && userId) {
    return (
      <SyncLoadingPage
        userId={userId}
        isFirstSync={isFirstSync}
        onSyncComplete={() => {
          // Sync complete, will redirect from SyncLoadingPage
        }}
      />
    );
  }

  if (loading) {
    return (
      <Center minH="100vh">
        <VStack spacing={4}>
          <Spinner
            thickness="4px"
            speed="0.65s"
            emptyColor="gray.200"
            color="orange.500"
            size="xl"
          />
          <Text color="gray.600">Completing Strava authentication...</Text>
        </VStack>
      </Center>
    );
  }

  if (error) {
    return (
      <Center minH="100vh">
        <VStack spacing={4} textAlign="center">
          <Heading as="h1" size="lg" color="red.600">
            Authentication Failed
          </Heading>
          <Text color="gray.600">{error}</Text>
          <ChakraLink
            href="/"
            color="orange.500"
            fontSize="md"
            fontWeight="semibold"
          >
            Return to home
          </ChakraLink>
        </VStack>
      </Center>
    );
  }

  return null;
}
