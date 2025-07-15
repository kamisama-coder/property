import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LLMComponent } from './llm.component';

describe('LLMComponent', () => {
  let component: LLMComponent;
  let fixture: ComponentFixture<LLMComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LLMComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LLMComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
