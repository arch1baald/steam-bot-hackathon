import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor() { }

  setUserId(val:string)
  {
      localStorage.setItem('USER_ID', val)
  }
  getUserId()
  {
    localStorage.getItem('USER_ID')
  }
}
