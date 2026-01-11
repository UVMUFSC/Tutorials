// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtop.h for the primary calling header

#ifndef VERILATED_VTOP___024ROOT_H_
#define VERILATED_VTOP___024ROOT_H_  // guard

#include "verilated.h"


class Vtop__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtop___024root final {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(x0_i,0,0);
    VL_IN8(x1_i,0,0);
    VL_IN8(x2_i,0,0);
    VL_IN8(x3_i,0,0);
    VL_IN8(sel_i,1,0);
    VL_OUT8(y_o,0,0);
    CData/*0:0*/ mux4x1__DOT__x0_i;
    CData/*0:0*/ mux4x1__DOT__x1_i;
    CData/*0:0*/ mux4x1__DOT__x2_i;
    CData/*0:0*/ mux4x1__DOT__x3_i;
    CData/*1:0*/ mux4x1__DOT__sel_i;
    CData/*0:0*/ mux4x1__DOT__y_o;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VicoFirstIteration;
    VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VicoTriggered;

    // INTERNAL VARIABLES
    Vtop__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vtop___024root(Vtop__Syms* symsp, const char* namep);
    ~Vtop___024root();
    VL_UNCOPYABLE(Vtop___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
