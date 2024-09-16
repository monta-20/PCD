import Ind from '../components/Main/index';
import Draw from '../components/Main/Drawer';
import Chart from 'chart.js/auto';
import React, { useRef, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Typography } from '@material-ui/core';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    margin: theme.spacing(2),
    padding: theme.spacing(2),
    height: '100%',
    position: 'relative',
    color: '#333333',
  },
  title: {
    marginBottom: theme.spacing(2),
    display: 'flex',
    alignItems: 'center',
    color: 'green',
  },
  subtitle: {
    marginBottom: theme.spacing(1),
    fontSize: '18px',
  },
  table: {
    minWidth: 650,
  },
  tableCell: {
    fontSize: '1.5rem',
    color: '#4d4d4d',
    fontWeight: 'bold',
  },
  tableHeaderCell: {
    fontSize: '1.7rem',
    color: '#0099ff',
    fontWeight: 'bold',
  },
  tableContainer: {
    backgroundColor: '#f2f2f2',
    padding: '1rem',
    borderRadius: '8px',
    boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',
    width: '70%',
    margin: theme.spacing(2),
  },
  graphContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '60%',
    width: '60%',
  },
}));

function BarChart(props) {
  const chartRef = useRef(null);
  const chartInstanceRef = useRef(null);

  const classes = useStyles();
  const rows = [
    { day: 'Next days', predictedPrice: props.D1},
    { day: 'In two days', predictedPrice: props.D2 },
    { day: 'In three days', predictedPrice: props.D3},
    { day: 'In four days', predictedPrice: props.D4 },
    { day: 'In five days', predictedPrice: props.D5 },
  ];

  useEffect(() => {
    if (chartRef && chartRef.current) {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
      }
      const myChartRef = chartRef.current.getContext('2d');
      chartInstanceRef.current = new Chart(myChartRef, {
        // Type de graphique
        type: 'line',
        // Les données
        data: {
          labels: props.ord,
          datasets: [
            {
              label: 'Close',
              data: props.abs,
              backgroundColor: 'rgba(120, 200, 100, 0.2)', // Update with the desired background color
              borderColor: 'rgba(120, 100, 50, 1)', // Update with the desired border color
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            y: {
              type: 'linear',
              beginAtZero: false,
              ticks: {
                callback:                function (value) {
                  return Number(value.toFixed(0));
                },
              },
            },
          },
          plugins: {
            title: {
              display: true,
              text: props.chartTitle,
            },
          },
          responsive: true,
          maintainAspectRatio: false,
        },
      });
    }
  }, [props.abs, props.ord, props.chartTitle]);

  return (
    <div className={classes.root} style ={{background:'rgba(255,255,242,1)'}}>
      <Draw />
      <Ind />
      <Typography variant="h1" style={{ color: 'rgba(220, 100, 120, 0.9)', marginTop: '100px' }}>
        {props.title}
      </Typography>
      <Typography variant="h2" style={{ color: 'rgba(5, 0, 18, 0.9)', margin: '30px' }}>
        Stay informed with real-time stock market trends at a glance.
      </Typography>

      <div className={classes.graphContainer}>
        <canvas ref={chartRef} style={{ width: '70%', height: '70%' }} />
      </div>

      <div className={classes.root}>
        <Typography variant="h3" style={{ color: 'rgba(45, 46, 89, 0.9)', margin: '30px' }}>
          We are excited to share the latest news with you
        </Typography>

        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <div style={{ backgroundColor: 'lightgray', padding: '10px', margin: '10px' }}>
            <Typography variant="h5" className={classes.title}>
              <code style={{ color: 'green' }}>{props.DateN1}</code>
            </Typography>
            <Typography variant="subtitle1" className={classes.subtitle}>
                 {props.N1}
            </Typography>
          </div>

          <div style={{ backgroundColor: 'lightblue', padding: '10px', margin: '10px' }}>
            <Typography variant="h5" className={classes.title}>
              <code style={{ color: 'blue' }}>{props.DateN2}</code>
            </Typography>
            <Typography variant="subtitle1" className={classes.subtitle}>
                           {props.N2}
            </Typography>
          </div>

          <div style={{ backgroundColor: 'lightpink', padding: '10px', margin: '10px' }}>
            <Typography variant="h5" className={classes.title}>
              <code style={{ color: 'red' }}>{props.DateN3}</code>
            </Typography>
            <Typography variant="subtitle1" className={classes.subtitle}>
                                    {props.N3}
            </Typography>
          </div>
        </div>
      </div>

      <Typography variant="h3" style={{ color: 'rgba(45, 46, 89, 0.9)', margin: '30px' }}>
      Explore 5-day predictions and make informed decisions based on accurate forecasts
      </Typography>

      <TableContainer component={Paper} className={classes.tableContainer}>
        <Table className={classes.table} aria-label="daily price table">
          <TableHead>
            <TableRow>
              <TableCell className={classes.tableHeaderCell}>Day</TableCell>
              <TableCell align="right" className={classes.tableHeaderCell}>Predicted Daily Price</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row) => (
              <TableRow key={row.day}>
                <TableCell component="th" scope="row" className={classes.tableCell}>{row.day}</TableCell>
                <TableCell align="right" className={classes.tableCell}>{row.predictedPrice}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}

export default BarChart;


