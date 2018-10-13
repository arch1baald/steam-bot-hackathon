import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-new-message',
  templateUrl: './new-message.component.html',
  styleUrls: ['./new-message.component.css']
})
export class NewMessageComponent implements OnInit {

  
constructor(private http:HttpClient) 
  {

  }
   ngOnInit() {
  }
  public sendMessageToSteam(text: string): void
  {
      this.http.post("https://steambot20181013015404.azurewebsites.net/sendall?messageText="+text,null).subscribe();
    
     //this.http.post("https://pivasbot.appspot.com/api/sendToFriends/",{"Message": text, "Id": 1}).subscribe();
  } 
}
