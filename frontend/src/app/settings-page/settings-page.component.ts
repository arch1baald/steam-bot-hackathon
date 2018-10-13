import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-settings-page',
  templateUrl: './settings-page.component.html',
  styleUrls: ['./settings-page.component.css']
})
export class SettingsPageComponent implements OnInit {

  constructor(private http:HttpClient) { }

  ngOnInit() {
    this.http.get("https://pivasbot.appspot.com/api/getSettings/").subscribe((data: any) => {
       // this.currFriends= data.data.profile_stats.all_matches;
       //this.matches=data.data.matches;
       this.botName=data.botName;
       this.botDiscription=data.botDiscription;
       this.botWelcome = data.botWelcome;
       this.botRespond = data.botRespond;
    });
  }
  public botName: string = "adhjcgauygscagscy";
  public botDiscription : string;
  public botWelcome : string;
  public botRespond : string;
  //public 

   public sendSettings(botName: string, botDiscription : string, botWelcome : string, botRespond : string): void
  {
      //this.http.post("https://steambot20181013015404.azurewebsites.net/sendall?messageText="+text,null).subscribe();
    
     //this.http.post("https://pivasbot.appspot.com/api/sendToFriends/",{"Message": text, "Id": 1}).subscribe();
  } 
  

}
