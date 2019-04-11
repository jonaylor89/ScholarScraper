import { TestBed, async } from '@angular/core/testing';
import { FormFieldOverviewExample } from './form-field-overview-example';

describe('FormFieldOverviewExample', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        FormFieldOverviewExample
      ],
    }).compileComponents();
  }));

  it('should create the app', () => {
    const fixture = TestBed.createComponent(FormFieldOverviewExample);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have as title 'ScholarScraperFE'`, () => {
    const fixture = TestBed.createComponent(FormFieldOverviewExample);
    const app = fixture.debugElement.componentInstance;
    expect(app.title).toEqual('ScholarScraperFE');
  });

  it('should render title in a h1 tag', () => {
    const fixture = TestBed.createComponent(FormFieldOverviewExample);
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('h1').textContent).toContain('Welcome to ScholarScraperFE!');
  });
});
