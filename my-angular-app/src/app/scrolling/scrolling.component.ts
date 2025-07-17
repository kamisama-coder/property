import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';


@Component({
  selector: 'app-scrolling',
  imports: [CommonModule,FormsModule,HttpClientModule],
  templateUrl: './scrolling.component.html',
  styleUrl: './scrolling.component.css'
})

export class ScrollingComponent {
  setup:any[] = []
  query:string = ''
  perfectindex:string = ''

  constructor(private route: ActivatedRoute, private http: HttpClient, private router: Router) {
     this.route.queryParams.subscribe(params => {
      this.perfectindex = params['index'];
    }); 
    console.log(`you friend is: ${this.perfectindex}`)
     this.http.get<any>('http://127.0.0.1:5000/system-server',{}).subscribe({
                next: (response) => {
                  this.setup = response;
                }
      })

  }

  gotomap(long:string,latt:string){
    this.router.navigate(['/maps'], {
    queryParams: { long: long, latt: latt }
  });
  }

  pics(id:number){
    this.router.navigate(['/pics'], {
    queryParams: { index: id }
   });
  }

  imformation(id:number){
    this.router.navigate(['/page'], {
    queryParams: { index: id }
   });
  }

  edit(id:number,user_id:string){
    this.router.navigate(['/editing'], {
    queryParams: { index: id,edit: true,user_id:user_id }
    });
  }

  handleIndependentInput(){
    this.http.post<any>('http://127.0.0.1:5000/clipsort',{query:this.query}).subscribe({
      next: (response) => {
          if(response.length == 0){
            alert("asshole query")
          }
          else{
            this.setup = response;
            alert("now your data will processed according to query")
          }
      }
    })
  }
}
