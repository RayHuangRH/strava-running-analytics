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

export default function AuthCallback() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
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

        // Redirect to dashboard
        router.push('/dashboard');
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error occurred');
        setLoading(false);
      }
    };

    handleCallback();
  }, [searchParams, router]);

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
