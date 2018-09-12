package br.upe.base;

public enum AmplifierType {
    L17_10CH, // Amplificador de linha com potência máxima de saída de 17 dBm,
	      // utilizando 10 canais
    L17_20CH, L17_40CH, L17_80CH, L21_40CH, P14_L21, // Desse amplificador em
						     // diante a máscara é
						     // apenas para 40ch
    B24, B21_L21,
    B21_L24, EDFA_1_STG, EDFA_1_STG_PAR, EDFA_1_STG_IMPAR, EDFA_2_STG, EDFA_2_2_STG, EDFA_2_PadTec, 
    EDFA_1_PadTec, EDFA_1_T1_PadTec, EDFA_1_T2_PadTec, EDFA_1_T3_PadTec, EDFA_1_T4_PadTec, EDFA_1_T5_PadTec, EDFA_1_T6_PadTec, 
    EDFA_1_T7_PadTec, EDFA_1_T8_PadTec, EDFA_1_T9_PadTec, EDFA_1_T10_PadTec, EDFA_1_T11_PadTec, EDFA_1_T12_PadTec, EDFA_1_T13_PadTec, 
    EDFA_1_T14_PadTec, EDFA_1_T15_PadTec, EDFA_1_T16_PadTec, EDFA_1_T21_PadTec, EDFA_1_T17_PadTec, EDFA_1_T20_PadTec, EDFA_1_T25_PadTec, EDFA_1_T30_PadTec, EDFA_1_Tm1_PadTec, EDFA_1_Tm2_PadTec, 
    EDFA_1_Tm3_PadTec, EDFA_1_Tm4_PadTec, EDFA_1_Tm5_PadTec, EDFA_1_Tm6_PadTec, EDFA_1_Tm7_PadTec, EDFA_1_Tm8_PadTec, EDFA_1_Tm9_PadTec, 
    EDFA_1_Tm10_PadTec, EDFA_1_Tm11_PadTec, EDFA_1_Tm12_PadTec, EDFA_1_Tm13_PadTec, EDFA_1_Tm14_PadTec, EDFA_1_Tm15_PadTec, EDFA_1_Tm16_PadTec, EDFA_1_Tm17_PadTec, EDFA_1_Tm18_PadTec, EDFA_1_Tm19_PadTec, EDFA_1_Tm20_PadTec, EDFA_1_Tm22_PadTec, EDFA_1_Tm25_PadTec, EDFA_1_Tm26_PadTec, EDFA_1_Tm30_PadTec, EDFA_2_T2_PadTec,
    EDFA_2_Tm0v5_PadTec,EDFA_2_Tm1v5_PadTec, EDFA_2_Tm2v5_PadTec, EDFA_2_Tm3v5_PadTec, EDFA_2_Tm4v5_PadTec,
    EDFA_2_Tm1_PadTec, EDFA_2_Tm2_PadTec, EDFA_2_Tm3_PadTec, EDFA_2_Tm4_PadTec, EDFA_2_Tm5_PadTec, EDFA_2_Tm8_PadTec 
}
