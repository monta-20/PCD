import Score from '../../pages/Score';
import React, { useState, useEffect, useRef } from "react";
import axios from 'axios';

const AETEC = () => {
  const [aetec, setAetec] = useState([]);
  const [aetec_forecast, setAetec_forecast] = useState([]);
  const chartRef = useRef(null);
 

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get("http://localhost:5001/aetec");
        setAetec(res.data);
      } catch (err) {
        console.log(err);
      }

      try {
        const ress = await axios.get("http://localhost:5001/aetec_forecast");
        setAetec_forecast(ress.data);
      } catch (err) {
        console.log(err);
      }
    };

    fetchData();
  }, []);
  const nonNullNews = aetec.filter(item => item && item.news);
  const firstNonNullNews = aetec.find(item => item && item.news) || {news: '', date: ''};
  const secondNonNullNews = nonNullNews.length > 1 ? nonNullNews[1] : {news: '', date: ''};
  const thirdNonNullNews = nonNullNews.length > 2 ? nonNullNews[2] : {news: '', date: ''};

  return (
    <>
      <canvas ref={chartRef} />
      <Score
        title="AETECH"
        ord={aetec.map((item) => item.date.split('T')[0])}
        abs={aetec.map((item) => item.close)}
        DateN1={firstNonNullNews.date.split('T')[0]}
        N1={firstNonNullNews.news} 
        DateN2={secondNonNullNews.date.split('T')[0]}
        N2={secondNonNullNews.news}
        DateN3={thirdNonNullNews.date.split('T')[0]}
        N3={thirdNonNullNews.news}
        D1={aetec_forecast[0]?.day_1}
        D2={aetec_forecast[0]?.day_2}
        D3={aetec_forecast[0]?.day_3}
        D4={aetec_forecast[0]?.day_4}
        D5={aetec_forecast[0]?.day_5}
      />
    </>
  );
};

export default AETEC;
