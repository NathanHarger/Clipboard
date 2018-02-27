import React, { Component } from 'react';
import axios from 'axios'
import FileDownload from 'react-file-download'
import logo from './logo.png';
import './App.css';
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
class App extends Component {
constructor(props) {
    super(props);
  this.getCookie = this.getCookie.bind(this);

  }
getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



  submit_text(){
      var csrft = this.getCookie('csrftoken')
      var data_text = this.text.value
      axios.post('/api/clipboard/',{
        
        text: data_text, csrftoken: csrft}
       
      )
      .then(function (response) {
        document.getElementById("container").innerHTML = response.data.id
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
  }

   

  submit_file(){
    var csrft = this.getCookie('csrftoken')
    var data_file = this.file
    var formData = new FormData();
    formData.append("file", data_file.files[0]);

    console.log(data_file.files[0])
    axios.post('/api/clipboard/', formData,{  headers: {
      'Content-Type': 'multipart/form-data'
    }})
    .then(function (response) {
      console.log(response);
      document.getElementById("container").innerHTML = response.data.id

    })
    .catch(function (error) {
      console.log(error);
    });
    alert(this.file.value)
    
  }


  submit_id(){
    var data_id = this.id.value
    var metadata;
    axios.get('/api/clipboard/getMetadata/', {params:{session_id: data_id}}) 
    .then(function (response) {
      metadata = response.data
      //console.log(response);
      //var media_type = response.data['media_type']
      //console.log(media_type)
      axios.get('/api/clipboard/getData/', {params:{session_id: data_id}})
        .then(function(response){
          console.log(response)
          if(metadata['media_type'] === "Text"){
            console.log("text")
            document.getElementById("container").innerHTML = response.data.data

          } else if(metadata['media_type'] === 'File'){
            console.log("file")

            FileDownload(response.data, metadata.FileMetaData['file_name']);
          }
        })

    })
    .catch(function (error) {
      console.log(error);
    });
    
  }


  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Anonymous Clipboard</h1>
        </header>
        
        <div className="App-center">
          <div className="App-forms">
            <form  noValidate>

              <label for="text">Enter Text:</label>
              <input name ="text" type='text' ref={(input) => this.text = input}></input>
            
              <input type="button" value= "Submit" onClick={this.submit_text.bind(this)} ></input>
            </form>

           
            <form encType="multipart/form-data" noValidate> 

            <label for="file"> Enter File: </label> 
              <input name ="file" type='file' ref={(input) => this.file = input}></input>
              <input type="button" value="Submit" onClick={this.submit_file.bind(this)}></input>
            </form>

            <form noValidate>  
              <label for="session_id">Enter Id:</label>
              <input type='text' name="session_id" ref={(input) => this.id = input}></input>
              <input type="button" value="Submit" onClick={this.submit_id.bind(this)}></input>
            </form>
          </div>
        </div>
        <div id="container">
        </div>
      </div>
    );
  }
}

export default App;

