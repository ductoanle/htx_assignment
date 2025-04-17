import React, { useState } from 'react';
import { Box, Button, Typography, CircularProgress, Alert, List, ListItem, ListItemText } from '@mui/material';
import { CloudUpload as CloudUploadIcon } from '@mui/icons-material';
import { uploadAudioFiles, Transcription } from '../services/api';

interface FileUploadProps {
  onUploadComplete: (transcriptions: Transcription[]) => void;
}

interface UploadResult {
  filename: string;
  status: 'success' | 'error';
  message?: string;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUploadComplete }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResults, setUploadResults] = useState<UploadResult[]>([]);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    setIsUploading(true);
    setUploadResults([]);

    try {
      const results = await uploadAudioFiles(Array.from(files));
      setUploadResults(results);
      
      // Extract successful transcriptions and notify parent
      const successfulTranscriptions = results
        .filter(result => result.status === 'success' && result.transcription)
        .map(result => result.transcription as Transcription);
      
      onUploadComplete(successfulTranscriptions);
    } catch (err) {
      console.error('Upload error:', err);
      const results = Array.from(files).map(file => ({
        filename: file.name,
        status: 'error' as const,
        message: 'Failed to upload file: Network error'
      }));
      setUploadResults(results);
    } finally {
      setIsUploading(false);
    }
  };

  const successCount = uploadResults.filter(result => result.status === 'success').length;
  const errorCount = uploadResults.filter(result => result.status === 'error').length;

  return (
    <Box>
      <Box sx={{ mb: 3 }}>
        <input
          accept="audio/*"
          style={{ display: 'none' }}
          id="audio-file-upload"
          multiple
          type="file"
          onChange={handleFileChange}
          disabled={isUploading}
        />
        <label htmlFor="audio-file-upload">
          <Button
            variant="contained"
            component="span"
            startIcon={isUploading ? <CircularProgress size={20} /> : <CloudUploadIcon />}
            disabled={isUploading}
          >
            {isUploading ? 'Uploading...' : 'Upload Audio Files'}
          </Button>
        </label>
      </Box>

      {uploadResults.length > 0 && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Upload Results
          </Typography>
          
          {successCount > 0 && (
            <Alert severity="success" sx={{ mb: 2 }}>
              Successfully processed {successCount} file(s)
            </Alert>
          )}
          
          {errorCount > 0 && (
            <Alert severity="error" sx={{ mb: 2 }}>
              Failed to process {errorCount} file(s)
            </Alert>
          )}
          
          <List>
            {uploadResults.map((result, index) => (
              <ListItem key={index} sx={{ 
                bgcolor: result.status === 'success' ? 'success.light' : 'error.light',
                mb: 1,
                borderRadius: 1
              }}>
                <ListItemText 
                  primary={result.filename}
                  secondary={
                    result.status === 'success' 
                      ? 'Successfully processed'
                      : result.message || 'Failed to process'
                  }
                />
              </ListItem>
            ))}
          </List>
        </Box>
      )}
    </Box>
  );
};

export default FileUpload; 