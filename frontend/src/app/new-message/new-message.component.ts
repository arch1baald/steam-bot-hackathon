import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {ModalViewComponent} from '../modal-view/modal-view.component';
import {Router} from '@angular/router'
import { UserService } from '../user.service'

import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material';
@Component({
  selector: 'app-new-message',
  templateUrl: './new-message.component.html',
  styleUrls: ['./new-message.component.css']
})
export class NewMessageComponent implements OnInit {

  
constructor(private http:HttpClient, private popup:MatDialog, private router:Router,private user:UserService) 
  {

  }
   ngOnInit() {
  }
  public sendMessageToSteam(text: string): void
  {
    this.http.post("https://pivasbot.appspot.com/api/sendToFriends/",{"Message": text, "Id": this.user.getUserId()}).subscribe();
      //this.http.post("https://steambot20181013015404.azurewebsites.net/sendall?messageText="+text,null).subscribe();
      this.displayPopup("kkkk");
    
     
  } 
  public displayPopup(text:string):void
  {
    this.popup.open(ModalViewComponent).afterClosed().subscribe(result => {
      this.router.navigate(["/dashboard"]);
    });;
  }
}
