import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import CSRFToken from './csrftoken';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Anonymous Clipboard</h1>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        <div className="App-center">
          <div className="App-forms">
            <form method="post" action='/api/clipboard/' novalidate>
              <CSRFToken />

              <label for="text">Enter Text:</label>
              <input name ="text" type='text'></input>
              <button type="submit">Submit</button>
            </form>

            <form method="post" action="/api/clipboard/" enctype="multipart/form-data" novalidate> 
            <CSRFToken />

            <label for="file"> Enter File: </label> 
            <input type="file" name="file"/> 
              <button type="submit">Submit</button>
            </form>

            <form action="/api/clipboard/getData" method="get" novalidate>  
              <label for="session_id">Enter Id:</label>
              <input type='text' name="session_id"></input>
              <button type="submit">Submit</button>
            </form>
          </div>
        </div>
      </div>
    );
  }
}

export default App;

