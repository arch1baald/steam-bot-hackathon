import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service'

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css']
})
export class LandingComponent implements OnInit {

  constructor(private user:UserService) { }

  ngOnInit() {
  }

}
