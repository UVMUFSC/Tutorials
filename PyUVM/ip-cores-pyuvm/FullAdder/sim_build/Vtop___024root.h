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
    VL_IN8(a_i,0,0);
    VL_IN8(b_i,0,0);
    VL_IN8(carry_i,0,0);
    VL_OUT8(sum_o,0,0);
    VL_OUT8(carry_o,0,0);
    CData/*0:0*/ full_adder__DOT__a_i;
    CData/*0:0*/ full_adder__DOT__b_i;
    CData/*0:0*/ full_adder__DOT__carry_i;
    CData/*0:0*/ full_adder__DOT__sum_o;
    CData/*0:0*/ full_adder__DOT__carry_o;
    CData/*0:0*/ full_adder__DOT__w_sum;
    CData/*0:0*/ full_adder__DOT__w_carry1;
    CData/*0:0*/ full_adder__DOT__w_carry2;
    CData/*0:0*/ full_adder__DOT__U1__DOT__a;
    CData/*0:0*/ full_adder__DOT__U1__DOT__b;
    CData/*0:0*/ full_adder__DOT__U1__DOT__c;
    CData/*0:0*/ full_adder__DOT__U1__DOT__s;
    CData/*0:0*/ full_adder__DOT__U2__DOT__a;
    CData/*0:0*/ full_adder__DOT__U2__DOT__b;
    CData/*0:0*/ full_adder__DOT__U2__DOT__c;
    CData/*0:0*/ full_adder__DOT__U2__DOT__s;
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
