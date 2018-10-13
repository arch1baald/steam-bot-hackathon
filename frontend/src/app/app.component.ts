import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent{
  title = 'SteamBot';

  constructor(private http:HttpClient) 
  {

  }
  
  public sendMessageToSteam(text: string): void
  {
    this.http.post("https://steambot20181013015404.azurewebsites.net/sendall?messageText="+text,null).subscribe();
    
   // this.http.post("http://127.0.0.1:8000/api/postMessage/",{"Message": text}).subscribe();
  } 

}

