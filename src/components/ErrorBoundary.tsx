import { Component, type ErrorInfo, type ReactNode } from 'react';
export class ErrorBoundary extends Component<{children:ReactNode},{failed:boolean}>{
 state={failed:false};
 static getDerivedStateFromError(){return {failed:true}}
 componentDidCatch(error:Error,info:ErrorInfo){console.error('Crop intelligence rendering error',error,info.componentStack)}
 render(){return this.state.failed?<main className="fatal-error"><h1>Unable to display this view</h1><p>The workbook data has not been changed. Reload the page to retry.</p><button className="action-button" onClick={()=>location.reload()}>Reload application</button></main>:this.props.children}
}
