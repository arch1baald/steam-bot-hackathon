import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {ModalViewComponent} from '../modal-view/modal-view.component';
import {Router} from '@angular/router';
import { UserService } from '../user.service';
//import {Location} from '@angular/common';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css']
})
export class LandingComponent implements OnInit {

  constructor(private http:HttpClient,  private router:Router,private user:UserService) { }

  ngOnInit() {
  }
  public sendLogin(text: string): void
  {

    //this.http.post("https://pivasbot.appspot.com/api/sendToFriends/",{"Message": text, "Id": this.user.getUserId()}).subscribe();
      //this.http.post("https://steambot20181013015404.azurewebsites.net/sendall?messageText="+text,null).subscribe();
      //this.displayPopup("kkkk");
      this.user.setUserId(text);
      //$route.reload();
    this.router.navigate(["/dashboard"]);
     window.location.reload();
    //this.location.reload();
     
  } 
}
