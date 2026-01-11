// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

void Vtop___024root___eval_triggers__ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_triggers__ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VicoTriggered[0U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VicoTriggered
                                      [0U]) | (IData)((IData)(vlSelfRef.__VicoFirstIteration)));
    vlSelfRef.__VicoFirstIteration = 0U;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtop___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
    }
#endif
}

bool Vtop___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___trigger_anySet__ico\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ico_sequent__TOP__0\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.adder_4bits__DOT__a_i = vlSelfRef.a_i;
    vlSelfRef.adder_4bits__DOT__b_i = vlSelfRef.b_i;
    vlSelfRef.adder_4bits__DOT__U3__DOT__a_i = (1U 
                                                & ((IData)(vlSelfRef.adder_4bits__DOT__a_i) 
                                                   >> 3U));
    vlSelfRef.adder_4bits__DOT__U2__DOT__a_i = (1U 
                                                & ((IData)(vlSelfRef.adder_4bits__DOT__a_i) 
                                                   >> 2U));
    vlSelfRef.adder_4bits__DOT__U0__DOT__a = (1U & (IData)(vlSelfRef.adder_4bits__DOT__a_i));
    vlSelfRef.adder_4bits__DOT__U1__DOT__a_i = (1U 
                                                & ((IData)(vlSelfRef.adder_4bits__DOT__a_i) 
                                                   >> 1U));
    vlSelfRef.adder_4bits__DOT__U3__DOT__b_i = (1U 
                                                & ((IData)(vlSelfRef.adder_4bits__DOT__b_i) 
                                                   >> 3U));
    vlSelfRef.adder_4bits__DOT__U2__DOT__b_i = (1U 
                                                & ((IData)(vlSelfRef.adder_4bits__DOT__b_i) 
                                                   >> 2U));
    vlSelfRef.adder_4bits__DOT__U0__DOT__b = (1U & (IData)(vlSelfRef.adder_4bits__DOT__b_i));
    vlSelfRef.adder_4bits__DOT__U1__DOT__b_i = (1U 
                                                & ((IData)(vlSelfRef.adder_4bits__DOT__b_i) 
                                                   >> 1U));
    vlSelfRef.adder_4bits__DOT__U3__DOT__U1__DOT__a 
        = vlSelfRef.adder_4bits__DOT__U3__DOT__a_i;
    vlSelfRef.adder_4bits__DOT__U2__DOT__U1__DOT__a 
        = vlSelfRef.adder_4bits__DOT__U2__DOT__a_i;
    vlSelfRef.adder_4bits__DOT__U1__DOT__U1__DOT__a 
        = vlSelfRef.adder_4bits__DOT__U1__DOT__a_i;
    vlSelfRef.adder_4bits__DOT__U3__DOT__U1__DOT__b 
        = vlSelfRef.adder_4bits__DOT__U3__DOT__b_i;
    vlSelfRef.adder_4bits__DOT__U2__DOT__U1__DOT__b 
        = vlSelfRef.adder_4bits__DOT__U2__DOT__b_i;
    vlSelfRef.adder_4bits__DOT__U0__DOT__s = ((IData)(vlSelfRef.adder_4bits__DOT__U0__DOT__a) 
                                              ^ (IData)(vlSelfRef.adder_4bits__DOT__U0__DOT__b));
    vlSelfRef.adder_4bits__DOT__U0__DOT__c = ((IData)(vlSelfRef.adder_4bits__DOT__U0__DOT__a) 
                                              & (IData)(vlSelfRef.adder_4bits__DOT__U0__DOT__b));
    vlSelfRef.adder_4bits__DOT__U1__DOT__U1__DOT__b 
        = vlSelfRef.adder_4bits__DOT__U1__DOT__b_i;
    vlSelfRef.adder_4bits__DOT__U3__DOT__U1__DOT__c 
        = ((IData)(vlSelfRef.adder_4bits__DOT__U3__DOT__U1__DOT__a) 
           & (IData)(vlSelfRef.adder_4bits__DOT__U3__DOT__U1__DOT__b));
    vlSelfRef.adder_4bits__DOT__U3__DOT__U1__DOT__s 
        = ((IData)(vlSelfRef.adder_4bits__DOT__U3__DOT__U1__DOT__a) 
           ^ (IData)(vlSelfRef.adder_4bits__DOT__U3__DOT__U1__DOT__b));
    vlSelfRef.adder_4bits__DOT__U2__DOT__U1__DOT__c 
        = ((IData)(vlSelfRef.adder_4bits__DOT__U2__DOT__U1__DOT__a) 
           & (IData)(vlSelfRef.adder_4bits__DOT__U2__DOT__U1__DOT__b));
    vlSelfRef.adder_4bits__DOT__U2__DOT__U1__DOT__s 
        = ((IData)(vlSelfRef.adder_4bits__DOT__U2__DOT__U1__DOT__a) 
           ^ (IData)(vlSelfRef.adder_4bits__DOT__U2__DOT__U1__DOT__b));
    vlSelfRef.adder_4bits__DOT__U1__DOT__carry_i = vlSelfRef.adder_4bits__DOT__U0__DOT__c;
    vlSelfRef.adder_4bits__DOT__U1__DOT__U1__DOT__c 
        = ((IData)(vlSelfRef.adder_4bits__DOT__U1__DOT__U1__DOT__a) 
           & (IData)(vlSelfRef.adder_4bits__DOT__U1__DOT__U1__DOT__b));
    vlSelfRef.adder_4bits__DOT__U1__DOT__U1__DOT__s 
        = ((IData)(vlSelfRef.adder_4bits__DOT__U1__DOT__U1__DOT__a) 
           ^ (IData)(vlSelfRef.adder_4bits__DOT__U1__DOT__U1__DOT__b));
    vlSelfRef.adder_4bits__DOT__U3__DOT__w_carry1 = vlSelfRef.adder_4bits__DOT__U3__DOT__U1__DOT__c;
    vlSelfRef.adder_4bits__DOT__U3__DOT__w_sum = vlSelfRef.adder_4bits__DOT__U3__DOT__U1__DOT__s;
    vlSelfRef.adder_4bits__DOT__U2__DOT__w_carry1 = vlSelfRef.adder_4bits__DOT__U2__DOT__U1__DOT__c;
    vlSelfRef.adder_4bits__DOT__U2__DOT__w_sum = vlSelfRef.adder_4bits__DOT__U2__DOT__U1__DOT__s;
    vlSelfRef.adder_4bits__DOT__U1__DOT__U2__DOT__b 
        = vlSelfRef.adder_4bits__DOT__U1__DOT__carry_i;
    vlSelfRef.adder_4bits__DOT__U1__DOT__w_carry1 = vlSelfRef.adder_4bits__DOT__U1__DOT__U1__DOT__c;
    vlSelfRef.adder_4bits__DOT__U1__DOT__w_sum = vlSelfRef.adder_4bits__DOT__U1__DOT__U1__DOT__s;
    vlSelfRef.adder_4bits__DOT__U3__DOT__U2__DOT__a 
        = vlSelfRef.adder_4bits__DOT__U3__DOT__w_sum;
    vlSelfRef.adder_4bits__DOT__U2__DOT__U2__DOT__a 
        = vlSelfRef.adder_4bits__DOT__U2__DOT__w_sum;
    vlSelfRef.adder_4bits__DOT__U1__DOT__U2__DOT__a 
        = vlSelfRef.adder_4bits__DOT__U1__DOT__w_sum;
    vlSelfRef.adder_4bits__DOT__U1__DOT__U2__DOT__s 
        = ((IData)(vlSelfRef.adder_4bits__DOT__U1__DOT__U2__DOT__a) 
           ^ (IData)(vlSelfRef.adder_4bits__DOT__U1__DOT__U2__DOT__b));
    vlSelfRef.adder_4bits__DOT__U1__DOT__U2__DOT__c 
        = ((IData)(vlSelfRef.adder_4bits__DOT__U1__DOT__U2__DOT__a) 
           & (IData)(vlSelfRef.adder_4bits__DOT__U1__DOT__U2__DOT__b));
    vlSelfRef.adder_4bits__DOT__U1__DOT__sum_o = vlSelfRef.adder_4bits__DOT__U1__DOT__U2__DOT__s;
    vlSelfRef.adder_4bits__DOT__U1__DOT__w_carry2 = vlSelfRef.adder_4bits__DOT__U1__DOT__U2__DOT__c;
    vlSelfRef.adder_4bits__DOT__U1__DOT__carry_o = 
        ((IData)(vlSelfRef.adder_4bits__DOT__U1__DOT__w_carry1) 
         | (IData)(vlSelfRef.adder_4bits__DOT__U1__DOT__w_carry2));
    vlSelfRef.adder_4bits__DOT__U2__DOT__carry_i = vlSelfRef.adder_4bits__DOT__U1__DOT__carry_o;
    vlSelfRef.adder_4bits__DOT__U2__DOT__U2__DOT__b 
        = vlSelfRef.adder_4bits__DOT__U2__DOT__carry_i;
    vlSelfRef.adder_4bits__DOT__U2__DOT__U2__DOT__s 
        = ((IData)(vlSelfRef.adder_4bits__DOT__U2__DOT__U2__DOT__a) 
           ^ (IData)(vlSelfRef.adder_4bits__DOT__U2__DOT__U2__DOT__b));
    vlSelfRef.adder_4bits__DOT__U2__DOT__U2__DOT__c 
        = ((IData)(vlSelfRef.adder_4bits__DOT__U2__DOT__U2__DOT__a) 
           & (IData)(vlSelfRef.adder_4bits__DOT__U2__DOT__U2__DOT__b));
    vlSelfRef.adder_4bits__DOT__U2__DOT__sum_o = vlSelfRef.adder_4bits__DOT__U2__DOT__U2__DOT__s;
    vlSelfRef.adder_4bits__DOT__U2__DOT__w_carry2 = vlSelfRef.adder_4bits__DOT__U2__DOT__U2__DOT__c;
    vlSelfRef.adder_4bits__DOT__U2__DOT__carry_o = 
        ((IData)(vlSelfRef.adder_4bits__DOT__U2__DOT__w_carry1) 
         | (IData)(vlSelfRef.adder_4bits__DOT__U2__DOT__w_carry2));
    vlSelfRef.adder_4bits__DOT__w_carry = (((IData)(vlSelfRef.adder_4bits__DOT__U2__DOT__carry_o) 
                                            << 2U) 
                                           | (((IData)(vlSelfRef.adder_4bits__DOT__U1__DOT__carry_o) 
                                               << 1U) 
                                              | (IData)(vlSelfRef.adder_4bits__DOT__U0__DOT__c)));
    vlSelfRef.adder_4bits__DOT__U3__DOT__carry_i = 
        (1U & ((IData)(vlSelfRef.adder_4bits__DOT__w_carry) 
               >> 2U));
    vlSelfRef.adder_4bits__DOT__U3__DOT__U2__DOT__b 
        = vlSelfRef.adder_4bits__DOT__U3__DOT__carry_i;
    vlSelfRef.adder_4bits__DOT__U3__DOT__U2__DOT__s 
        = ((IData)(vlSelfRef.adder_4bits__DOT__U3__DOT__U2__DOT__a) 
           ^ (IData)(vlSelfRef.adder_4bits__DOT__U3__DOT__U2__DOT__b));
    vlSelfRef.adder_4bits__DOT__U3__DOT__U2__DOT__c 
        = ((IData)(vlSelfRef.adder_4bits__DOT__U3__DOT__U2__DOT__a) 
           & (IData)(vlSelfRef.adder_4bits__DOT__U3__DOT__U2__DOT__b));
    vlSelfRef.adder_4bits__DOT__U3__DOT__sum_o = vlSelfRef.adder_4bits__DOT__U3__DOT__U2__DOT__s;
    vlSelfRef.adder_4bits__DOT__U3__DOT__w_carry2 = vlSelfRef.adder_4bits__DOT__U3__DOT__U2__DOT__c;
    vlSelfRef.adder_4bits__DOT__s_o = ((((IData)(vlSelfRef.adder_4bits__DOT__U3__DOT__sum_o) 
                                         << 3U) | ((IData)(vlSelfRef.adder_4bits__DOT__U2__DOT__sum_o) 
                                                   << 2U)) 
                                       | (((IData)(vlSelfRef.adder_4bits__DOT__U1__DOT__sum_o) 
                                           << 1U) | (IData)(vlSelfRef.adder_4bits__DOT__U0__DOT__s)));
    vlSelfRef.adder_4bits__DOT__U3__DOT__carry_o = 
        ((IData)(vlSelfRef.adder_4bits__DOT__U3__DOT__w_carry1) 
         | (IData)(vlSelfRef.adder_4bits__DOT__U3__DOT__w_carry2));
    vlSelfRef.s_o = vlSelfRef.adder_4bits__DOT__s_o;
    vlSelfRef.adder_4bits__DOT__c_o = vlSelfRef.adder_4bits__DOT__U3__DOT__carry_o;
    vlSelfRef.c_o = vlSelfRef.adder_4bits__DOT__c_o;
}

void Vtop___024root___eval_ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VicoTriggered[0U])) {
        Vtop___024root___ico_sequent__TOP__0(vlSelf);
    }
}

bool Vtop___024root___eval_phase__ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VicoExecute;
    // Body
    Vtop___024root___eval_triggers__ico(vlSelf);
    __VicoExecute = Vtop___024root___trigger_anySet__ico(vlSelfRef.__VicoTriggered);
    if (__VicoExecute) {
        Vtop___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

void Vtop___024root___eval(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VicoIterCount;
    // Body
    __VicoIterCount = 0U;
    vlSelfRef.__VicoFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00000064U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
            VL_FATAL_MT("/home/edu17z/Documents/Projeto_UVM/PyUVM/Adder4Bits/adder_4bits.sv", 1, "", "Input combinational region did not converge after 100 tries");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
    } while (Vtop___024root___eval_phase__ico(vlSelf));
}

#ifdef VL_DEBUG
void Vtop___024root___eval_debug_assertions(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_debug_assertions\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.a_i & 0xf0U)))) {
        Verilated::overWidthError("a_i");
    }
    if (VL_UNLIKELY(((vlSelfRef.b_i & 0xf0U)))) {
        Verilated::overWidthError("b_i");
    }
}
#endif  // VL_DEBUG
