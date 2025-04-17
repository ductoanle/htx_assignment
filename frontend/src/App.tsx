import React, { useEffect, useState } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  CssBaseline, 
  ThemeProvider, 
  createTheme,
  Tabs,
  Tab,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  InputAdornment,
  Alert
} from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import HealthStatus from './components/HealthStatus';
import FileUpload from './components/FileUpload';
import { getAllTranscriptions, searchTranscriptions, Transcription } from './services/api';

const theme = createTheme({
  palette: {
    mode: 'light',
  },
});

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

interface ParsedFilename {
  baseName: string;
  version: number | null;
}

function parseFilename(filename: string): ParsedFilename {
  const versionMatch = filename.match(/_ver_(\d+)\./);
  if (versionMatch) {
    const version = parseInt(versionMatch[1], 10);
    const baseName = filename.replace(/_ver_\d+\./, '.');
    return { baseName, version };
  }
  return { baseName: filename, version: null };
}

function TranscriptionTable({ transcriptions }: { transcriptions: Transcription[] }) {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>File Name</TableCell>
            <TableCell>Version</TableCell>
            <TableCell>Text</TableCell>
            <TableCell>Created Date</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {transcriptions.length > 0 ? (
            transcriptions.map((transcription) => {
              const { baseName, version } = parseFilename(transcription.audio_file_name);
              return (
                <TableRow key={transcription.id}>
                  <TableCell>{baseName}</TableCell>
                  <TableCell>{version !== null ? version : '-'}</TableCell>
                  <TableCell>{transcription.transcribed_text}</TableCell>
                  <TableCell>{formatDate(transcription.created_at)}</TableCell>
                </TableRow>
              );
            })
          ) : (
            <TableRow>
              <TableCell colSpan={4} align="center">
                No transcriptions found
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

function App() {
  const [transcriptions, setTranscriptions] = useState<Transcription[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchResults, setSearchResults] = useState<Transcription[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [tabValue, setTabValue] = useState(0);
  const [recentUploads, setRecentUploads] = useState<Transcription[]>([]);

  const loadTranscriptions = async () => {
    try {
      const data = await getAllTranscriptions();
      setTranscriptions(data);
    } catch (error) {
      console.error('Failed to load transcriptions:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadTranscriptions();
  }, []);

  const handleUploadComplete = (newTranscriptions: Transcription[]) => {
    setTranscriptions((prev) => [...newTranscriptions, ...prev]);
    setRecentUploads(newTranscriptions);
  };

  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }

    try {
      const results = await searchTranscriptions(query);
      setSearchResults(results);
    } catch (error) {
      console.error('Search failed:', error);
    }
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            HTX Transcriber
          </Typography>
          <HealthStatus />
          
          <Box sx={{ borderBottom: 1, borderColor: 'divider', mt: 3 }}>
            <Tabs value={tabValue} onChange={handleTabChange} aria-label="transcription tabs">
              <Tab label="Upload Audio Files" />
              <Tab label="All Transcriptions" />
              <Tab label="Search Transcriptions" />
            </Tabs>
          </Box>
          
          <TabPanel value={tabValue} index={0}>
            <FileUpload onUploadComplete={handleUploadComplete} />
            
            {recentUploads.length > 0 && (
              <Box sx={{ mt: 4 }}>
                <Typography variant="h6" gutterBottom>
                  Recent Uploads
                </Typography>
                <TranscriptionTable transcriptions={recentUploads} />
              </Box>
            )}
          </TabPanel>
          
          <TabPanel value={tabValue} index={1}>
            {isLoading ? (
              <Typography>Loading transcriptions...</Typography>
            ) : (
              <TranscriptionTable transcriptions={transcriptions} />
            )}
          </TabPanel>
          
          <TabPanel value={tabValue} index={2}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Search by audio file name..."
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value)}
              sx={{ mb: 3 }}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
              }}
            />
            
            {searchQuery && (
              <TranscriptionTable transcriptions={searchResults} />
            )}
          </TabPanel>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
