import * as React from 'react';
import AvatarGroup from '@mui/joy/AvatarGroup';
import Avatar from '@mui/joy/Avatar';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Typography from '@mui/joy/Typography';
import ArrowForward from '@mui/icons-material/ArrowForward';
import TwoSidedLayout from '../components/TwoSidedLayout';

export default function HomePage() {
  return (
    <TwoSidedLayout>
      <Typography color="primary" fontSize="lg" fontWeight="lg">
        Discover the Art of Tomorrow
      </Typography>
      <Typography
        level="h1"
        fontWeight="xl"
        fontSize="clamp(1.875rem, 1.3636rem + 2.1818vw, 3rem)"
      >
        Explore a World of Creativity with Our Art Gallery App
      </Typography>
      <Typography fontSize="lg" textColor="text.secondary" lineHeight="lg">
        Dive into an expansive collection of contemporary and classic art. Find your inspiration, connect with artists, and purchase original artwork with ease.
      </Typography>
      <Box
        sx={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: 2,
          my: 2,
          '& > *': { flex: 'auto' },
        }}
      >
        <Button size="lg" variant="outlined" color="neutral">
          Discover More
        </Button>
        <Button size="lg" endDecorator={<ArrowForward fontSize="xl" />}>
          Join Now
        </Button>
      </Box>
      <Box
        sx={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: 2,
          textAlign: 'left',
          '& > *': {
            flexShrink: 0,
          },
        }}
      >
        <AvatarGroup size="lg">
          <Avatar />
          <Avatar />
          <Avatar />
        </AvatarGroup>
        <Typography textColor="text.secondary">
          Become part of a growing community of over <b>20K</b> <br />
          art lovers, collectors, and artists.
        </Typography>
      </Box>
      <Typography
        level="body-xs"
        sx={{
          position: 'absolute',
          top: '2rem',
          left: '50%',
          transform: 'translateX(-50%)',
        }}
      >        
      </Typography>
    </TwoSidedLayout>
  );
}
