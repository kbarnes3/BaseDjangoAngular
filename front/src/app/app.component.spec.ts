import { TestBed, waitForAsync } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';
import { Component, ChangeDetectionStrategy } from '@angular/core';
import { NavBarComponent } from './nav-bar/nav-bar.component';

@Component({
    selector: 'app-nav-bar',
    changeDetection: ChangeDetectionStrategy.OnPush,
    template: '<p>Nav Bar</p>',
    
})
class MockNavBarComponent {
}

describe('AppComponent', () => {
  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule
      ],
    })
    .overrideComponent(AppComponent, {
      remove: {
        imports: [NavBarComponent]
      },
      add: {
        imports: [MockNavBarComponent]
      }
    })
    .compileComponents();
  }));

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have as title 'NewDjangoSite'`, () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app.title).toEqual('NewDjangoSite');
  });

});
