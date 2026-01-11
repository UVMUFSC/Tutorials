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
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        VL_IN8(a_i,3,0);
        VL_IN8(b_i,3,0);
        VL_OUT8(s_o,3,0);
        VL_OUT8(c_o,0,0);
        CData/*3:0*/ adder_4bits__DOT__a_i;
        CData/*3:0*/ adder_4bits__DOT__b_i;
        CData/*3:0*/ adder_4bits__DOT__s_o;
        CData/*0:0*/ adder_4bits__DOT__c_o;
        CData/*2:0*/ adder_4bits__DOT__w_carry;
        CData/*0:0*/ adder_4bits__DOT__U0__DOT__a;
        CData/*0:0*/ adder_4bits__DOT__U0__DOT__b;
        CData/*0:0*/ adder_4bits__DOT__U0__DOT__c;
        CData/*0:0*/ adder_4bits__DOT__U0__DOT__s;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__a_i;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__b_i;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__carry_i;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__sum_o;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__carry_o;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__w_sum;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__w_carry1;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__w_carry2;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__U1__DOT__a;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__U1__DOT__b;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__U1__DOT__c;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__U1__DOT__s;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__U2__DOT__a;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__U2__DOT__b;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__U2__DOT__c;
        CData/*0:0*/ adder_4bits__DOT__U1__DOT__U2__DOT__s;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__a_i;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__b_i;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__carry_i;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__sum_o;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__carry_o;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__w_sum;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__w_carry1;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__w_carry2;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__U1__DOT__a;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__U1__DOT__b;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__U1__DOT__c;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__U1__DOT__s;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__U2__DOT__a;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__U2__DOT__b;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__U2__DOT__c;
        CData/*0:0*/ adder_4bits__DOT__U2__DOT__U2__DOT__s;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__a_i;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__b_i;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__carry_i;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__sum_o;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__carry_o;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__w_sum;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__w_carry1;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__w_carry2;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__U1__DOT__a;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__U1__DOT__b;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__U1__DOT__c;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__U1__DOT__s;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__U2__DOT__a;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__U2__DOT__b;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__U2__DOT__c;
        CData/*0:0*/ adder_4bits__DOT__U3__DOT__U2__DOT__s;
        CData/*0:0*/ __VstlFirstIteration;
        CData/*0:0*/ __VicoFirstIteration;
        VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
    };
    struct {
        VlUnpacked<QData/*63:0*/, 1> __VicoTriggered;
    };

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
