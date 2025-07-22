import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Alert,
  LinearProgress
} from '@mui/material';
import {
  CheckCircle,
  Error,
  Warning,
  Security,
  Code,
  TrendingUp
} from '@mui/icons-material';

interface AnalysisIssue {
  file: string;
  line: number;
  message: string;
  code?: string;
  severity?: string;
}

interface SecurityIssue {
  file: string;
  line: number;
  pattern: string;
  severity: string;
}

interface AnalysisResults {
  score: number;
  static_analysis: {
    errors: AnalysisIssue[];
    warnings: AnalysisIssue[];
  };
  security: {
    secrets: SecurityIssue[];
    vulnerabilities: any[];
  };
  suggestions: string[];
}

interface AnalysisReportProps {
  results: AnalysisResults;
  loading?: boolean;
}

const AnalysisReport: React.FC<AnalysisReportProps> = ({ results, loading = false }) => {
  const { 
    score = 0, 
    static_analysis = { errors: [], warnings: [] }, 
    security = { secrets: [], vulnerabilities: [] }, 
    suggestions = [] 
  } = results || {};

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'success';
    if (score >= 70) return 'warning';
    return 'error';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 90) return <CheckCircle color="success" />;
    if (score >= 70) return <Warning color="warning" />;
    return <Error color="error" />;
  };

  if (loading) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Analyzing...
          </Typography>
          <LinearProgress />
        </CardContent>
      </Card>
    );
  }

  return (
    <Box>
      {/* 總體評分 */}
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Box display="flex" alignItems="center" gap={2} mb={2}>
            {getScoreIcon(score)}
            <Typography variant="h5" component="h2">
              Code Quality Score
            </Typography>
          </Box>
          
          <Box display="flex" alignItems="center" gap={2}>
            <Typography variant="h3" color={getScoreColor(score)}>
              {score}/100
            </Typography>
            <Chip 
              label={score >= 90 ? 'Excellent' : score >= 70 ? 'Good' : 'Needs Improvement'}
              color={getScoreColor(score)}
              variant="outlined"
            />
          </Box>
          
          <LinearProgress 
            variant="determinate" 
            value={score} 
            color={getScoreColor(score)}
            sx={{ mt: 2, height: 8, borderRadius: 4 }}
          />
        </CardContent>
      </Card>

      {/* 靜態分析結果 */}
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Box display="flex" alignItems="center" gap={1} mb={2}>
            <Code />
            <Typography variant="h6">Static Analysis Results</Typography>
          </Box>

          {static_analysis.errors.length > 0 && (
            <Alert severity="error" sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                {static_analysis.errors.length} error(s) found
              </Typography>
              <List dense>
                {static_analysis.errors.slice(0, 5).map((error, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <Error color="error" />
                    </ListItemIcon>
                    <ListItemText
                      primary={error.message}
                      secondary={`${error.file}:${error.line} ${error.code || ''}`}
                    />
                  </ListItem>
                ))}
              </List>
            </Alert>
          )}

          {static_analysis.warnings.length > 0 && (
            <Alert severity="warning" sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                {static_analysis.warnings.length} warning(s) found
              </Typography>
              <List dense>
                {static_analysis.warnings.slice(0, 5).map((warning, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <Warning color="warning" />
                    </ListItemIcon>
                    <ListItemText
                      primary={warning.message}
                      secondary={`${warning.file}:${warning.line} ${warning.code || ''}`}
                    />
                  </ListItem>
                ))}
              </List>
            </Alert>
          )}

          {static_analysis.errors.length === 0 && static_analysis.warnings.length === 0 && (
            <Alert severity="success">
              No static analysis issues found
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* 安全檢查 */}
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Box display="flex" alignItems="center" gap={1} mb={2}>
            <Security />
            <Typography variant="h6">Security Check</Typography>
          </Box>

          {security.secrets.length > 0 && (
            <Alert severity="error" sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                {security.secrets.length} potential security issue(s) found
              </Typography>
              <List dense>
                {security.secrets.slice(0, 3).map((secret, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <Security color="error" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Hardcoded secret detected"
                      secondary={`${secret.file}:${secret.line} - ${secret.pattern}`}
                    />
                  </ListItem>
                ))}
              </List>
            </Alert>
          )}

          {security.secrets.length === 0 && (
            <Alert severity="success">
              No security vulnerabilities found
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* 改進建議 */}
      {suggestions.length > 0 && (
        <Card>
          <CardContent>
            <Box display="flex" alignItems="center" gap={1} mb={2}>
              <TrendingUp />
              <Typography variant="h6">Suggestions for Improvement</Typography>
            </Box>
            
            <List>
              {suggestions.map((suggestion, index) => (
                <React.Fragment key={index}>
                  <ListItem>
                    <ListItemIcon>
                      <TrendingUp color="primary" />
                    </ListItemIcon>
                    <ListItemText primary={suggestion} />
                  </ListItem>
                  {index < suggestions.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default AnalysisReport; 