import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginLinksComponent } from './login-links.component';

describe('LoginLinksComponent', () => {
  let component: LoginLinksComponent;
  let fixture: ComponentFixture<LoginLinksComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LoginLinksComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginLinksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
