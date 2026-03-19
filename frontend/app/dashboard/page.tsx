'use client';

import { useEffect, useState } from 'react';
import {
  Box,
  Container,
  Flex,
  Heading,
  Text,
  Button,
  Center,
  VStack,
  HStack,
  Image,
  Grid,
  GridItem,
  Card,
  CardBody,
  Code,
  Spinner,
  Link as ChakraLink,
} from '@chakra-ui/react';

interface AthleteData {
  id: number;
  username: string;
  firstname: string;
  lastname: string;
  profile_medium: string;
  profile: string;
}

export default function Dashboard() {
  const [athlete, setAthlete] = useState<AthleteData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const athleteData = localStorage.getItem('athleteData');
    if (athleteData) {
      setAthlete(JSON.parse(athleteData));
    }
    setLoading(false);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('athleteData');
    window.location.href = '/';
  };

  if (loading) {
    return (
      <Center minH="100vh">
        <Spinner
          thickness="4px"
          speed="0.65s"
          emptyColor="gray.200"
          color="orange.500"
          size="lg"
        />
      </Center>
    );
  }

  if (!athlete) {
    return (
      <Center minH="100vh">
        <VStack spacing={4} textAlign="center">
          <Text color="gray.600">No athlete data found</Text>
          <ChakraLink href="/" color="orange.500" fontWeight="semibold">
            Return to login
          </ChakraLink>
        </VStack>
      </Center>
    );
  }

  return (
    <Box minH="100vh" bg="gray.50">
      {/* Header */}
      <Box bg="white" boxShadow="md" py={4}>
        <Container maxW="7xl">
          <Flex justify="space-between" align="center">
            <Heading as="h1" size="xl" color="gray.900">
              Running Dashboard
            </Heading>
            <Button onClick={handleLogout} colorScheme="red" size="md">
              Logout
            </Button>
          </Flex>
        </Container>
      </Box>

      {/* Main Content */}
      <Container maxW="7xl" py={8}>
        {/* Athlete Profile Card */}
        <Card mb={8}>
          <CardBody>
            <HStack spacing={4} align="start">
              {athlete.profile && (
                <Image
                  src={athlete.profile}
                  alt={athlete.firstname}
                  borderRadius="full"
                  w="24"
                  h="24"
                  objectFit="cover"
                />
              )}
              <VStack align="start" spacing={1}>
                <Heading as="h2" size="md" color="gray.900">
                  {athlete.firstname} {athlete.lastname}
                </Heading>
                <Text color="gray.600">@{athlete.username}</Text>
              </VStack>
            </HStack>
          </CardBody>
        </Card>

        {/* Dashboard Grid */}
        <Grid
          templateColumns={{
            base: '1fr',
            md: 'repeat(2, 1fr)',
            lg: 'repeat(3, 1fr)',
          }}
          gap={6}
          mb={8}
        >
          {/* Activities Card */}
          <Card>
            <CardBody>
              <Heading as="h3" size="md" color="gray.900" mb={2}>
                Activities
              </Heading>
              <Text fontSize="3xl" fontWeight="bold" color="orange.500">
                Coming Soon
              </Text>
              <Text color="gray.600" fontSize="sm" mt={1}>
                Your recent activities
              </Text>
            </CardBody>
          </Card>

          {/* Statistics Card */}
          <Card>
            <CardBody>
              <Heading as="h3" size="md" color="gray.900" mb={2}>
                Statistics
              </Heading>
              <Text fontSize="3xl" fontWeight="bold" color="blue.500">
                Coming Soon
              </Text>
              <Text color="gray.600" fontSize="sm" mt={1}>
                Monthly and yearly stats
              </Text>
            </CardBody>
          </Card>

          {/* Goals Card */}
          <Card>
            <CardBody>
              <Heading as="h3" size="md" color="gray.900" mb={2}>
                Goals
              </Heading>
              <Text fontSize="3xl" fontWeight="bold" color="green.500">
                Coming Soon
              </Text>
              <Text color="gray.600" fontSize="sm" mt={1}>
                Track your running goals
              </Text>
            </CardBody>
          </Card>
        </Grid>

        {/* Debug Info */}
        <Card bg="gray.100">
          <CardBody>
            <Heading as="h3" size="sm" color="gray.700" mb={2}>
              Debug Info
            </Heading>
            <Code
              p={3}
              borderRadius="md"
              display="block"
              overflowX="auto"
              fontSize="xs"
              color="gray.600"
            >
              {JSON.stringify(athlete, null, 2)}
            </Code>
          </CardBody>
        </Card>
      </Container>
    </Box>
  );
}
