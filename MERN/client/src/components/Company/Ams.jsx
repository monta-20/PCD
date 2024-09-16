import Score from '../../pages/Score';
import React, { useState, useEffect, useRef } from "react";
import axios from 'axios';
const AMS = () => {
  const [ams, setAms] = useState([]);
  const [ams_forecast, setAms_forecast] = useState([]);
  const chartRef = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get("http://localhost:5001/ams");
        setAms(res.data);
      } catch (err) {
        console.log(err);
      }

      try {
        const ress = await axios.get("http://localhost:5001/ams_forecast");
        setAms_forecast(ress.data);
      } catch (err) {
        console.log(err);
      }
    };

    fetchData();
  }, []);
  const nonNullNews = ams.filter(item => item && item.news);
  const firstNonNullNews = ams.find(item => item && item.news) || {news: '', date: ''};
  const secondNonNullNews = nonNullNews.length > 1 ? nonNullNews[1] : {news: '', date: ''};
  const thirdNonNullNews = nonNullNews.length > 2 ? nonNullNews[2] : {news: '', date: ''};
  return (
    <>
      <canvas ref={chartRef} />
      <Score  title="AMS" 
              ord={ams.slice(0, 50).map((item) => item.date.split('T')[0])}
              abs={ams.slice(0, 50).map((item) => item.close)}
              DateN1={firstNonNullNews.date.split('T')[0]}
              N1={firstNonNullNews.news} 
              DateN2={secondNonNullNews.date.split('T')[0]}
              N2={secondNonNullNews.news}
              DateN3={thirdNonNullNews.date.split('T')[0]}
              N3={thirdNonNullNews.news}
              D1={ams_forecast[0]?.day_1}
              D2={ams_forecast[0]?.day_2}
              D3={ams_forecast[0]?.day_3}
              D4={ams_forecast[0]?.day_4}
              D5={ams_forecast[0]?.day_5}  />
 </>
 );
};

export default AMS;