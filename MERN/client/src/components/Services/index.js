import React, { useState, useEffect } from "react";
import { useTheme } from "@mui/material";
import "./SearchBar.css";
import SearchIcon from "@mui/icons-material/Search";
import CloseIcon from "@mui/icons-material/Close";
import data from "../../Data.json";

function SearchComponent({ placeholder }) {
  const theme = useTheme();
  const [filteredData, setFilteredData] = useState([]);
  const [wordEntered, setWordEntered] = useState("");
  const [options, setOptions] = useState([]);

  useEffect(() => {
    setOptions(data);
  }, []);

  const handleFilter = (event) => {
    const searchWord = event.target.value;
    setWordEntered(searchWord);
    const newFilter = data.filter((value) => {
      return value.title.toLowerCase().includes(searchWord.toLowerCase());
    });

    if (searchWord === "") {
      setFilteredData([]);
    } else {
      setFilteredData(newFilter);
    }
  };

  const clearInput = () => {
    setFilteredData([]);
    setWordEntered("");
  };
    const handleOptionSelect = (event) => {
      const selectedOption = event.target.value;
      const selectedData = data.find((value) => {
        return value.title === selectedOption;
      });
  
      const url = `http://localhost:3000/${selectedData.link}`;

      // Navigate to the new URL
      window.location.href = url;  
    };    
  

  return (
    <div className="search" style={{ backgroundColor: theme.palette.background.alt }}>
      <div className="searchInputs">
        <input
          type="text"
          placeholder={placeholder}
          value={wordEntered}
          onChange={handleFilter}
        />
        <div className="searchIcon">
          {filteredData.length === 0 ? (
            <SearchIcon />
          ) : (
            <CloseIcon id="clearBtn" onClick={clearInput} />
          )}
        </div>
      </div>
      {filteredData.length !== 0 && (
        <div className="dataResult">
          {filteredData.slice(0, 15).map((value, key) => {
            return (
              <a className="dataItem" href={value.link} rel="noreferrer">
                <p>{value.title} </p>
              </a>
            );
          })}
        </div>
      )}
      {options.length !== 0 && (
        <div className="selectContainer">
          <select value={wordEntered} onChange={handleOptionSelect}>
            <option value="">Select a Company</option>
            {options.map((option, index) => {
              return (
                <option key={index} value={option.title}>
                  {option.title}
                </option>
              );
            })}
          </select>
        </div>
      )}
    </div>
  );
}

export default SearchComponent;
