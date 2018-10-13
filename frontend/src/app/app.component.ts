import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { UserService } from './user.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent{
  title = 'SteamBot';

  constructor(private http:HttpClient,private user:UserService) 
  {
    this.userName=user.getUserId();
  }
  public userName;

}

