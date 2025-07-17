import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-llm',
  imports: [CommonModule,FormsModule,HttpClientModule],
  templateUrl: './llm.component.html',
  styleUrl: './llm.component.css'
})
export class LLMComponent {

  query:string = '';
  error:boolean = false;
  errorfound:string = '';
  index:string = '';

  constructor(private http: HttpClient,private router: Router, private route: ActivatedRoute){
    this.route.queryParams.subscribe(params => {
      this.index = params['index'] ||  null;
    });
  }

  ngOnInit(){

  }

  onsearch(){
    this.http.post<any>('http://127.0.0.1:5000/gemini', {query:this.query}).subscribe({

          next: (response) => {
           if (response?.error) {
              this.errorfound = response.error;
              this.error = true;
            }
            else{
             this.router.navigate(['/scroll'], {
             queryParams: { index: this.index }
            })
            }
          },
          error: () => {
            console.error("AJAX error occurred.");
          }
        });
  }
}
