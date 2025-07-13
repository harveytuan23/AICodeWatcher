import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Button,
  TextField,
  Alert,
  Paper,
  Tabs,
  Tab
} from '@mui/material';
import {
  GitHub,
  Code,
  Security,
  TrendingUp,
  PlayArrow,
  Settings
} from '@mui/icons-material';
import AnalysisReport from '../components/AnalysisReport';

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

const Dashboard: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [repoUrl, setRepoUrl] = useState('');
  const [analysisResults, setAnalysisResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleAnalyzeRepo = async () => {
    if (!repoUrl.trim()) {
      setError('請輸入倉庫 URL');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // 這裡應該調用後端 API
      const response = await fetch('/api/v1/analysis/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ repo_url: repoUrl }),
      });

      if (!response.ok) {
        throw new Error('分析失敗');
      }

      const results = await response.json();
      setAnalysisResults(results);
    } catch (err) {
      setError(err instanceof Error ? err.message : '分析失敗');
    } finally {
      setLoading(false);
    }
  };

  const mockAnalysisResults = {
    results: {
      score: 85,
      static_analysis: {
        errors: [
          {
            file: 'main.py',
            line: 15,
            message: '未定義的變量',
            code: 'E0602'
          },
          {
            file: 'utils.py',
            line: 42,
            message: '導入未使用的模塊',
            code: 'F401'
          }
        ],
        warnings: [
          {
            file: 'config.py',
            line: 8,
            message: '行太長',
            code: 'E501'
          }
        ]
      },
      security: {
        secrets: [
          {
            file: 'config.py',
            line: 12,
            pattern: 'api_key',
            severity: 'high'
          }
        ],
        vulnerabilities: []
      },
      suggestions: [
        '修復未定義的變量錯誤',
        '移除未使用的導入',
        '使用環境變量替代硬編碼的 API 密鑰',
        '考慮添加更多的單元測試'
      ]
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center">
        🤖 CodeWatcher AI
      </Typography>
      <Typography variant="h6" color="text.secondary" align="center" gutterBottom>
        自動化 AI 代碼審查和可靠性平台
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="功能標籤">
          <Tab label="代碼分析" icon={<Code />} />
          <Tab label="GitHub 集成" icon={<GitHub />} />
          <Tab label="安全檢查" icon={<Security />} />
          <Tab label="設置" icon={<Settings />} />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  手動代碼分析
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  輸入 GitHub 倉庫 URL 進行代碼分析
                </Typography>
                
                <TextField
                  fullWidth
                  label="GitHub 倉庫 URL"
                  variant="outlined"
                  value={repoUrl}
                  onChange={(e) => setRepoUrl(e.target.value)}
                  placeholder="https://github.com/username/repo"
                  sx={{ mb: 2 }}
                />
                
                <Button
                  variant="contained"
                  startIcon={<PlayArrow />}
                  onClick={handleAnalyzeRepo}
                  disabled={loading}
                  fullWidth
                >
                  {loading ? '分析中...' : '開始分析'}
                </Button>

                {error && (
                  <Alert severity="error" sx={{ mt: 2 }}>
                    {error}
                  </Alert>
                )}
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  功能特色
                </Typography>
                <Box>
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    <Code color="primary" />
                    <Typography variant="body2">靜態代碼分析</Typography>
                  </Box>
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    <Security color="primary" />
                    <Typography variant="body2">安全漏洞檢測</Typography>
                  </Box>
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    <TrendingUp color="primary" />
                    <Typography variant="body2">代碼質量評分</Typography>
                  </Box>
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    <GitHub color="primary" />
                    <Typography variant="body2">自動 PR 評論</Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            {analysisResults ? (
              <AnalysisReport results={analysisResults.results || analysisResults} loading={loading} />
            ) : (
              <Paper sx={{ p: 3, textAlign: 'center' }}>
                <Typography variant="h6" color="text.secondary">
                  開始分析以查看結果
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  或者查看示例結果
                </Typography>
                <Button
                  variant="outlined"
                  onClick={() => setAnalysisResults(mockAnalysisResults)}
                  sx={{ mt: 2 }}
                >
                  查看示例
                </Button>
              </Paper>
            )}
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  GitHub Webhook 設置
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  配置 GitHub webhook 以自動分析 PR
                </Typography>
                
                <Alert severity="info" sx={{ mb: 2 }}>
                  <Typography variant="body2">
                    Webhook URL: <code>https://your-domain.com/api/v1/webhooks/github</code>
                  </Typography>
                </Alert>
                
                <Button variant="contained" fullWidth>
                  查看設置指南
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  最近分析記錄
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  暫無分析記錄
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <Typography variant="h6" gutterBottom>
          安全檢查功能
        </Typography>
        <Typography variant="body2" color="text.secondary">
          檢測硬編碼密鑰、安全漏洞等問題
        </Typography>
      </TabPanel>

      <TabPanel value={tabValue} index={3}>
        <Typography variant="h6" gutterBottom>
          系統設置
        </Typography>
        <Typography variant="body2" color="text.secondary">
          配置 GitHub Token、分析規則等
        </Typography>
      </TabPanel>
    </Container>
  );
};

export default Dashboard; 