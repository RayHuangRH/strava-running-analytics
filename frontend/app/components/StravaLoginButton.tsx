import Link from 'next/link';
import { Box, Button, HStack } from '@chakra-ui/react';
import Image from 'next/image';

interface StravaLoginButtonProps {
  redirectUri?: string;
}

export default function StravaLoginButton({
  redirectUri = 'http://localhost:3000/auth/callback',
}: StravaLoginButtonProps) {
  const clientId = process.env.NEXT_PUBLIC_STRAVA_CLIENT_ID;
  const scope = 'activity:read_all,profile:read_all';

  // Construct Strava OAuth authorization URL
  const stravaAuthUrl = new URL('https://www.strava.com/oauth/authorize');
  stravaAuthUrl.searchParams.append('client_id', clientId || '');
  stravaAuthUrl.searchParams.append('redirect_uri', redirectUri);
  stravaAuthUrl.searchParams.append('response_type', 'code');
  stravaAuthUrl.searchParams.append('approval_prompt', 'force');
  stravaAuthUrl.searchParams.append('scope', scope);

  return (
    <Link href={stravaAuthUrl.toString()}>
      <Button
        px={4}
        bg="orange.500"
        color="white"
        _hover={{ bg: 'orange.600' }}
        size="lg"
        fontSize="md"
        fontWeight="semibold"
      >
        <Box>
          <img
            src="/icons/strava.svg"
            alt="Strava Logo"
            width={20}
            height={20}
          />
        </Box>
        Login with Strava
      </Button>
    </Link>
  );
}
