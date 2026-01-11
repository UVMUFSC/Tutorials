// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"

VL_ATTR_COLD void Vtop___024root___eval_static(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_static\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vtop___024root___eval_initial(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_initial\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vtop___024root___eval_final(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_final\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vtop___024root___eval_phase__stl(Vtop___024root* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_settle(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_settle\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00000064U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("/home/edu17z/Documents/Projeto_UVM/PyUVM/Adder4Bits/adder_4bits.sv", 1, "", "Settle region did not converge after 100 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
    } while (Vtop___024root___eval_phase__stl(vlSelf));
}

VL_ATTR_COLD void Vtop___024root___eval_triggers__stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_triggers__stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VstlTriggered
                                      [0U]) | (IData)((IData)(vlSelfRef.__VstlFirstIteration)));
    vlSelfRef.__VstlFirstIteration = 0U;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtop___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
}

VL_ATTR_COLD bool Vtop___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vtop___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vtop___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___trigger_anySet__stl\n"); );
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

void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
        Vtop___024root___ico_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD bool Vtop___024root___eval_phase__stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    Vtop___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = Vtop___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        Vtop___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

bool Vtop___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (IData)(Vtop___024root___trigger_anySet__ico(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtop___024root___ctor_var_reset(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ctor_var_reset\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->a_i = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 12042468572559684522ull);
    vlSelf->b_i = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15122488259574687123ull);
    vlSelf->s_o = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4621052662690795927ull);
    vlSelf->c_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16113469836849596107ull);
    vlSelf->adder_4bits__DOT__a_i = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 10289909070645988615ull);
    vlSelf->adder_4bits__DOT__b_i = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 15613058569787223064ull);
    vlSelf->adder_4bits__DOT__s_o = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8277235435593419293ull);
    vlSelf->adder_4bits__DOT__c_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3662369795868370159ull);
    vlSelf->adder_4bits__DOT__w_carry = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 842043911293415374ull);
    vlSelf->adder_4bits__DOT__U0__DOT__a = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9779426203798267107ull);
    vlSelf->adder_4bits__DOT__U0__DOT__b = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 460967977079763555ull);
    vlSelf->adder_4bits__DOT__U0__DOT__c = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5332189776621121279ull);
    vlSelf->adder_4bits__DOT__U0__DOT__s = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1307147397624927994ull);
    vlSelf->adder_4bits__DOT__U1__DOT__a_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3143023203596551224ull);
    vlSelf->adder_4bits__DOT__U1__DOT__b_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8432300327292559120ull);
    vlSelf->adder_4bits__DOT__U1__DOT__carry_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7769648681583670629ull);
    vlSelf->adder_4bits__DOT__U1__DOT__sum_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6237612060212706452ull);
    vlSelf->adder_4bits__DOT__U1__DOT__carry_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13281338771936584641ull);
    vlSelf->adder_4bits__DOT__U1__DOT__w_sum = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4577163078301529106ull);
    vlSelf->adder_4bits__DOT__U1__DOT__w_carry1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1735909048915698157ull);
    vlSelf->adder_4bits__DOT__U1__DOT__w_carry2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6898754959819125287ull);
    vlSelf->adder_4bits__DOT__U1__DOT__U1__DOT__a = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1131898057340358144ull);
    vlSelf->adder_4bits__DOT__U1__DOT__U1__DOT__b = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10837042160234812302ull);
    vlSelf->adder_4bits__DOT__U1__DOT__U1__DOT__c = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17516733362487159318ull);
    vlSelf->adder_4bits__DOT__U1__DOT__U1__DOT__s = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12707456307073959827ull);
    vlSelf->adder_4bits__DOT__U1__DOT__U2__DOT__a = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17142694341735286139ull);
    vlSelf->adder_4bits__DOT__U1__DOT__U2__DOT__b = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5792541963467103358ull);
    vlSelf->adder_4bits__DOT__U1__DOT__U2__DOT__c = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10539089545258166098ull);
    vlSelf->adder_4bits__DOT__U1__DOT__U2__DOT__s = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9481740556781282324ull);
    vlSelf->adder_4bits__DOT__U2__DOT__a_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12366051573992932765ull);
    vlSelf->adder_4bits__DOT__U2__DOT__b_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1334640534808380868ull);
    vlSelf->adder_4bits__DOT__U2__DOT__carry_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1452366853626138122ull);
    vlSelf->adder_4bits__DOT__U2__DOT__sum_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9866896592872706317ull);
    vlSelf->adder_4bits__DOT__U2__DOT__carry_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15055970567080963825ull);
    vlSelf->adder_4bits__DOT__U2__DOT__w_sum = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6572683908247552598ull);
    vlSelf->adder_4bits__DOT__U2__DOT__w_carry1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3467781533983977016ull);
    vlSelf->adder_4bits__DOT__U2__DOT__w_carry2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15366060667078933268ull);
    vlSelf->adder_4bits__DOT__U2__DOT__U1__DOT__a = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13064171158373205296ull);
    vlSelf->adder_4bits__DOT__U2__DOT__U1__DOT__b = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6816564505781745916ull);
    vlSelf->adder_4bits__DOT__U2__DOT__U1__DOT__c = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 259584232318204593ull);
    vlSelf->adder_4bits__DOT__U2__DOT__U1__DOT__s = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4864316190770775671ull);
    vlSelf->adder_4bits__DOT__U2__DOT__U2__DOT__a = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2882675792246620304ull);
    vlSelf->adder_4bits__DOT__U2__DOT__U2__DOT__b = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4380365128518257786ull);
    vlSelf->adder_4bits__DOT__U2__DOT__U2__DOT__c = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6915081733293186594ull);
    vlSelf->adder_4bits__DOT__U2__DOT__U2__DOT__s = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15229652233687587581ull);
    vlSelf->adder_4bits__DOT__U3__DOT__a_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13265089673591230989ull);
    vlSelf->adder_4bits__DOT__U3__DOT__b_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6125133249760580846ull);
    vlSelf->adder_4bits__DOT__U3__DOT__carry_i = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10189905948599493971ull);
    vlSelf->adder_4bits__DOT__U3__DOT__sum_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3320001690849032555ull);
    vlSelf->adder_4bits__DOT__U3__DOT__carry_o = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15509713468430235380ull);
    vlSelf->adder_4bits__DOT__U3__DOT__w_sum = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11211391285470050164ull);
    vlSelf->adder_4bits__DOT__U3__DOT__w_carry1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7567514498654725850ull);
    vlSelf->adder_4bits__DOT__U3__DOT__w_carry2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17894244380828928404ull);
    vlSelf->adder_4bits__DOT__U3__DOT__U1__DOT__a = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14100405340143179519ull);
    vlSelf->adder_4bits__DOT__U3__DOT__U1__DOT__b = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7305248095425529348ull);
    vlSelf->adder_4bits__DOT__U3__DOT__U1__DOT__c = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11306944305958552439ull);
    vlSelf->adder_4bits__DOT__U3__DOT__U1__DOT__s = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17333440902719550214ull);
    vlSelf->adder_4bits__DOT__U3__DOT__U2__DOT__a = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3879608026715272436ull);
    vlSelf->adder_4bits__DOT__U3__DOT__U2__DOT__b = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14064462511520052184ull);
    vlSelf->adder_4bits__DOT__U3__DOT__U2__DOT__c = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5438281650777763940ull);
    vlSelf->adder_4bits__DOT__U3__DOT__U2__DOT__s = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8602346331807710362ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VicoTriggered[__Vi0] = 0;
    }
}
