import React, { useEffect, useState } from 'react';
import { Box, Typography, CircularProgress } from '@mui/material';
import { checkHealth } from '../services/api';

const HealthStatus: React.FC = () => {
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);

  useEffect(() => {
    const checkSystemHealth = async () => {
      const healthy = await checkHealth();
      setIsHealthy(healthy);
    };

    checkSystemHealth();
    const interval = setInterval(checkSystemHealth, 30000); // Check every 30 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
      <Typography variant="subtitle1">System Status:</Typography>
      {isHealthy === null ? (
        <CircularProgress size={20} />
      ) : isHealthy ? (
        <Typography color="success.main">Healthy</Typography>
      ) : (
        <Typography color="error.main">Unhealthy</Typography>
      )}
    </Box>
  );
};

export default HealthStatus; 