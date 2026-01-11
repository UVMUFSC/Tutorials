// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__pch.h"

Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(124);
    // Setup sub module instances
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscopep_TOP = new VerilatedScope{this, "TOP", "TOP", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_full_adder = new VerilatedScope{this, "full_adder", "full_adder", "full_adder", -9, VerilatedScope::SCOPE_MODULE};
    __Vscopep_full_adder__U1 = new VerilatedScope{this, "full_adder.U1", "U1", "half_adder", -9, VerilatedScope::SCOPE_MODULE};
    __Vscopep_full_adder__U2 = new VerilatedScope{this, "full_adder.U2", "U2", "half_adder", -9, VerilatedScope::SCOPE_MODULE};
    // Set up scope hierarchy
    __Vhier.add(0, __Vscopep_full_adder);
    __Vhier.add(__Vscopep_full_adder, __Vscopep_full_adder__U1);
    __Vhier.add(__Vscopep_full_adder, __Vscopep_full_adder__U2);
    // Setup export functions - final: 0
    // Setup export functions - final: 1
    // Setup public variables
    __Vscopep_TOP->varInsert("a_i", &(TOP.a_i), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("b_i", &(TOP.b_i), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("carry_i", &(TOP.carry_i), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("carry_o", &(TOP.carry_o), false, VLVT_UINT8, VLVD_OUT|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("sum_o", &(TOP.sum_o), false, VLVT_UINT8, VLVD_OUT|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder->varInsert("a_i", &(TOP.full_adder__DOT__a_i), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder->varInsert("b_i", &(TOP.full_adder__DOT__b_i), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder->varInsert("carry_i", &(TOP.full_adder__DOT__carry_i), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder->varInsert("carry_o", &(TOP.full_adder__DOT__carry_o), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder->varInsert("sum_o", &(TOP.full_adder__DOT__sum_o), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder->varInsert("w_carry1", &(TOP.full_adder__DOT__w_carry1), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder->varInsert("w_carry2", &(TOP.full_adder__DOT__w_carry2), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder->varInsert("w_sum", &(TOP.full_adder__DOT__w_sum), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder__U1->varInsert("a", &(TOP.full_adder__DOT__U1__DOT__a), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder__U1->varInsert("b", &(TOP.full_adder__DOT__U1__DOT__b), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder__U1->varInsert("c", &(TOP.full_adder__DOT__U1__DOT__c), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder__U1->varInsert("s", &(TOP.full_adder__DOT__U1__DOT__s), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder__U2->varInsert("a", &(TOP.full_adder__DOT__U2__DOT__a), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder__U2->varInsert("b", &(TOP.full_adder__DOT__U2__DOT__b), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder__U2->varInsert("c", &(TOP.full_adder__DOT__U2__DOT__c), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_full_adder__U2->varInsert("s", &(TOP.full_adder__DOT__U2__DOT__s), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
}

Vtop__Syms::~Vtop__Syms() {
    // Tear down scope hierarchy
    __Vhier.remove(0, __Vscopep_full_adder);
    __Vhier.remove(__Vscopep_full_adder, __Vscopep_full_adder__U1);
    __Vhier.remove(__Vscopep_full_adder, __Vscopep_full_adder__U2);
    // Tear down scopes
    VL_DO_CLEAR(delete __Vscopep_TOP, __Vscopep_TOP = nullptr);
    VL_DO_CLEAR(delete __Vscopep_full_adder, __Vscopep_full_adder = nullptr);
    VL_DO_CLEAR(delete __Vscopep_full_adder__U1, __Vscopep_full_adder__U1 = nullptr);
    VL_DO_CLEAR(delete __Vscopep_full_adder__U2, __Vscopep_full_adder__U2 = nullptr);
    // Tear down sub module instances
}
