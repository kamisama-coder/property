import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-wallpaper',
  imports: [CommonModule,FormsModule,HttpClientModule],
  templateUrl: './wallpaper.component.html',
  styleUrl: './wallpaper.component.css'
})
export class WallpaperComponent {
   setup:any[] = []
   pageid:string = ''


    constructor(private route: ActivatedRoute, private http: HttpClient, private router: Router) {
     this.route.queryParams.subscribe(params => {
      this.pageid = params['index']
    });  
     this.http.get<any>('http://127.0.0.1:5000/page',{params:{index : this.pageid}}).subscribe({
                next: (response) => {
                  this.setup = response;
                }
      })

  }

}
