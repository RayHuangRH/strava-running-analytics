import {
  Box,
  Container,
  VStack,
  Heading,
  Text,
  Center,
} from '@chakra-ui/react';
import StravaLoginButton from './components/StravaLoginButton';

async function getData() {
  const res = await fetch('http://localhost:8000');
  return res.json();
}

export default async function Home() {
  const data = await getData();

  return (
    <Box
      minH="100vh"
      bgGradient="linear(to-br, gray.50, gray.100)"
      display="flex"
      alignItems="center"
      justifyContent="center"
      px={4}
    >
      <Container maxW="md" centerContent>
        <Box bg="white" borderRadius="lg" boxShadow="lg" p={8} w="full">
          <VStack spacing={8} align="center">
            <Box textAlign="center">
              <Heading as="h1" size="2xl" mb={2} color="gray.900">
                Strava Running Analytics
              </Heading>
              <Text color="gray.600">{data.message}</Text>
            </Box>

            <VStack spacing={4} w="full" align="center">
              <Text fontSize="sm" color="gray.600" textAlign="center">
                Track your running activities and metrics in one place.
              </Text>

              <StravaLoginButton />

              <Text fontSize="xs" color="gray.500" textAlign="center" pt={4}>
                We use Strava to securely access your activity data. We don't
                store your password.
              </Text>
            </VStack>
          </VStack>
        </Box>
      </Container>
    </Box>
  );
}
